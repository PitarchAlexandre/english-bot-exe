import os
import re
import time
import json
import threading
import sounddevice as sd
from scipy.io.wavfile import write
import whisper as wp
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, scrolledtext
from speech_manager import SpeechManager
from ai_client import AiClient
from env_manager import EnvManager
from voice_manager import VoiceManager
from ielts_manager import IELTSManager


class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("IELTS Speaking Trainer")
        self.geometry("1000x700")

        self.env_manager = EnvManager()
        self.env_manager.load()
        self.api_key = self.env_manager.get("ENV_API_KEY")
        self.base_url = self.env_manager.get("ENV_BASE_URL")
        self.model = self.env_manager.get("ENV_AI_MODEL")

        self.ai_client = AiClient(self.api_key, self.base_url, self.model)
        self.voice_manager = VoiceManager()
        self.speech_manager = SpeechManager()

        self.discussion = []
        self.question_index = 0
        self.question_list = []

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=RIGHT, fill=Y, padx=10)

        self.create_left_widgets()
        self.create_right_widgets()
        
    def open_add_model_window(self):
        add_model_window = ttk.Toplevel(self)
        add_model_window.title("Ajouter un nouveau modèle IA")
        add_model_window.geometry("400x300")

        ttk.Label(add_model_window, text="API Key:").pack(pady=5)
        api_key_entry = ttk.Entry(add_model_window, width=40)
        api_key_entry.pack(pady=5)

        ttk.Label(add_model_window, text="Nom du modèle IA:").pack(pady=5)
        model_entry = ttk.Entry(add_model_window, width=40)
        model_entry.pack(pady=5)

        ttk.Label(add_model_window, text="Base URL:").pack(pady=5)
        base_url_entry = ttk.Entry(add_model_window, width=40)
        base_url_entry.pack(pady=5)

        def save_model():
            api_key = api_key_entry.get()
            model = model_entry.get()
            base_url = base_url_entry.get()

            if not all([api_key, model, base_url]):
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return

            # Update env_manager
            self.env_manager.set("ENV_API_KEY", api_key)
            self.env_manager.set("ENV_AI_MODEL", model)
            self.env_manager.set("ENV_BASE_URL", base_url)

            # Recréer AiClient avec les nouvelles infos
            self.ai_client = AiClient(api_key, base_url, model)

            messagebox.showinfo("Succès", "Le nouveau modèle IA a été enregistré avec succès.")
            add_model_window.destroy()

        button_frame = ttk.Frame(add_model_window)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Ajouter le modèle", bootstyle=SUCCESS, command=save_model).pack(side=LEFT, padx=10)
        ttk.Button(button_frame, text="Annuler", bootstyle=DANGER, command=add_model_window.destroy).pack(side=RIGHT, padx=10)

        
    def create_left_widgets(self):
        self.text_display = scrolledtext.ScrolledText(self.left_frame, wrap='word', height=30)
        self.text_display.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.time_remaining_label = ttk.Label(self.left_frame, text="Time Remaining: --:--", font=("Helvetica", 14))
        self.time_remaining_label.pack(pady=5)

    def create_right_widgets(self):
        ttk.Button(self.right_frame, text="Insérer un nouveau modèle IA", bootstyle=WARNING, command=self.open_add_model_window).pack(pady=5)
        self.label_level = ttk.Label(self.right_frame, text="Level:")
        self.label_level.pack(pady=5)
        self.level_var = ttk.StringVar(value="B1")
        for lvl in ["B1", "B2", "C1"]:
            ttk.Radiobutton(self.right_frame, text=lvl, variable=self.level_var, value=lvl).pack(pady=2)

        self.label_mode = ttk.Label(self.right_frame, text="Do you want to:")
        self.label_mode.pack(pady=5)
        self.mode_var = ttk.StringVar(value="write")
        ttk.Radiobutton(self.right_frame, text="Write", variable=self.mode_var, value="write").pack(pady=2)
        ttk.Radiobutton(self.right_frame, text="Speak", variable=self.mode_var, value="speak").pack(pady=2)

        self.label_theme = ttk.Label(self.right_frame, text="Theme:")
        self.label_theme.pack(pady=5)
        self.combo_theme = ttk.Combobox(self.right_frame, values=[
                                                                    "family",
                                                                    "hobbies",
                                                                    "school life",
                                                                    "technology",
                                                                    "health",
                                                                    "travel",
                                                                    "education",
                                                                    "work and career",
                                                                    "environment",
                                                                    "globalization",
                                                                    "artificial intelligence",
                                                                    "cultural identity",
                                                                    "tradition and values",
                                                                    "freedom of speech",
                                                                    "healthcare responsibility"
                                                                ]
                                                            )
        self.combo_theme.set("Technology")
        self.combo_theme.pack(pady=5)

        self.label_voice = ttk.Label(self.right_frame, text="Voice:")
        self.label_voice.pack(pady=5)
        self.voice_map = {f"{i+1}. {v['name']} ({v['country']}) - {v['gender']}": v['shortName'] for i, v in enumerate(self.voice_manager.voices)}
        self.combo_voice = ttk.Combobox(self.right_frame, values=list(self.voice_map.keys()))
        self.combo_voice.set(list(self.voice_map.keys())[0])
        self.combo_voice.pack(pady=5)

        self.start_btn = ttk.Button(self.right_frame, text="Start", bootstyle=SUCCESS, command=self.start_interview)
        self.start_btn.pack(pady=10)

        self.quit_btn = ttk.Button(self.right_frame, text="Quit", bootstyle=SECONDARY, command=self.quit)
        self.quit_btn.pack(pady=10)

    def update_text_display(self, text):
        self.text_display.insert('end', text + '\n')
        self.text_display.see('end')

    def update_time_remaining(self, time_left):
        minutes = time_left // 60
        seconds = time_left % 60
        self.time_remaining_label.config(text=f"Time Remaining: {minutes:02}:{seconds:02}")

    def start_interview(self):
        self.question_index = 0
        self.discussion = []
        theme = self.combo_theme.get()
        level = self.level_var.get()

        self.chosen_voice = self.voice_map[self.combo_voice.get()]
        voice_info = next(voice for voice in self.voice_manager.voices if voice['shortName'] == self.chosen_voice)
        name = voice_info['name']
        country = voice_info['country']

        self.ielts_manager = IELTSManager(level, theme, name, country)
        self.question_list = self.ielts_manager.generate_ordered_ielts_questions(theme, name, country)

        system_prompt = {
            "role": "system",
            "content": f"You are an IELTS examiner helping a student prepare for their IELTS speaking exam.\n\nThe goal is to achieve a {level} level on the topic \"{theme}\".\n\n✨ Your rules:\n- Evaluate only based on the user's answers.\n- Score from 1 to 9.\n- Give score per IELTS criteria and summary."
        }
        self.discussion.append(system_prompt)
        threading.Thread(target=self.ask_next_question).start()

    def ask_next_question(self):
        while self.question_index < len(self.question_list):
            part, question, duration = self.question_list[self.question_index]

            if part == "Prep":
                self.update_text_display(f"\n⏳ {question}")
                self.speech_manager.say_and_play(question, self.chosen_voice)
                for t in range(int(duration), 0, -1):
                    self.update_time_remaining(t)
                    time.sleep(1)
                self.question_index += 1
                continue

            self.update_text_display(f"\n🗂️ {part} — {question}")
            self.speech_manager.say_and_play(question, self.chosen_voice)
            self.discussion.append({"role": "assistant", "content": question})

            if self.mode_var.get() == "speak":
                self.update_text_display("🎙️ Speak now...")

                def countdown_timer(duration):
                    for t in range(duration, 0, -1):
                        self.update_time_remaining(t)
                        time.sleep(1)

                # Start countdown in parallel
                countdown_thread = threading.Thread(target=countdown_timer, args=(int(duration),))
                countdown_thread.start()

                # Start recording
                recording = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
                sd.wait()
                write("user_speech.wav", 44100, recording)

                # Ensure countdown finishes too
                countdown_thread.join()
               
                
                result = wp.load_model("base").transcribe("user_speech.wav")
                user_response = result["text"]
                self.update_text_display("📝 You said: " + user_response)

            else:
                user_response = self.simple_prompt_input()

            clean_response = re.sub(r"\([^)]*\)|\*[^*]*\*", "", user_response).strip()
            self.discussion.append({"role": "user", "content": clean_response})

            self.question_index += 1

            if part == "Part 1" and self.question_index == 5:
                self.update_text_display("\n🎯 You have now finished part 1. Let's move to Part 2.")
                self.speech_manager.say_and_play("You have now finished part 1. Let's move to Part 2.", self.chosen_voice)
            elif part == "Part 2":
                self.update_text_display("\n🚀 You have now finished part 2! Now, let's move to Part 3.")
                self.speech_manager.say_and_play("You have now finished part 2! Now, let's move to Part 3.", self.chosen_voice)
            elif part == "Part 3" and self.question_index == 10:
                self.update_text_display("\n🎉 Well done! Now, let's proceed to the evaluation.")
                self.speech_manager.say_and_play("Well done! Now, let's proceed to the evaluation.", self.chosen_voice)

        evaluation = self.ai_client.evaluate(self.discussion)
        self.update_text_display("\n📊 Evaluation:\n" + evaluation)

    def simple_prompt_input(self):
        prompt_win = ttk.Toplevel(self)
        prompt_win.title("Your Answer")
        answer_var = ttk.StringVar()
        prompt_entry = ttk.Entry(prompt_win, width=80, textvariable=answer_var)
        prompt_entry.pack(pady=10, padx=10)

        def confirm():
            prompt_win.destroy()

        ttk.Button(prompt_win, text="Submit", command=confirm).pack(pady=5)
        prompt_entry.focus()
        prompt_win.grab_set()
        self.wait_window(prompt_win)
        return answer_var.get()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
