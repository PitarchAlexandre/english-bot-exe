import time
import re

class IELTSManager:
    def __init__(self, level_chosen, theme_chosen, name, country):
        self.level_chosen = level_chosen
        self.theme_chosen = theme_chosen
        self.name = name
        self.country = country
        self.question_list = self.generate_ordered_ielts_questions(theme_chosen, name, country)
        self.disscussion = []

    def generate_ordered_ielts_questions(self, theme, name, country):
        """Génère les questions IELTS basées sur le thème choisi et les informations sur l'examinateur."""
        return [
            ("Part 1", f"""Hello, my name is {name} and I come from {country}. I am your examiner.\n
                Now, introduce yourself""", 25),
            ("Part 1", f"What do you like about {theme}?", 30),
            ("Part 1", f"How often do you talk about {theme}?", 30),
            ("Part 1", f"Is {theme} important in your life?", 30),
            ("Part 1", f"When did you first get interested in {theme}?", 30),
            ("Prep", f"""You now have 60 seconds to read the following questions.\n
                         After that, you have to answer the following question:\n \n
                         Describe a memorable experience you had with {theme}.\n 
                         Who was involved?\n 
                         Why was it memorable?\n""", 60),
            ("Part 2", "Now, please begin speaking.", 90),
            ("Part 3", f"How has {theme} changed in society over time?", 60),
            ("Part 3", f"What challenges are linked to {theme}?", 60),
            ("Part 3", f"Do different cultures view {theme} differently?", 60),
            ("Evaluation", "Let's now evaluate your performance.", 0)
        ]
    def start_interview(self, say_and_play, user_speech):
        """Lance l'interview avec les questions IELTS."""
        question_index = 0

        while question_index < len(self.question_list):
            current_part, current_question, duration = self.question_list[question_index]

            if current_part == "Prep":
                print(f"\n⏳ {current_question}")
                say_and_play(current_question)
                time.sleep(duration)
                question_index += 1
                continue

            print(f"\n🗂️ {current_part} — {current_question}")
            say_and_play(current_question)

            self.disscussion.append({"role": "assistant", "content": current_question})

            if user_speech == "write":
                message = input("- ")
            else:
                print("🎙️ Speak now...")
                message = self.record_audio(duration)

            if message.strip().upper() == "!STOP":
                print("👋 Goodbye!")
                break

            # Nettoyer la réponse
            clean_response = re.sub(r"\([^)]*\)|\*[^*]*\*", "", message).strip()
            self.disscussion.append({"role": "user", "content": clean_response})

            question_index += 1
