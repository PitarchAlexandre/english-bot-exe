import os
import re
import time
import json
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
import whisper
from speech_manager import SpeechManager
from ai_client import AiClient
from env_manager import EnvManager
from voice_manager import VoiceManager
from ielts_manager import IELTSManager

# Load environment variables
env_manager = EnvManager()
env_manager.load()
BASE_URL = env_manager.get("ENV_BASE_URL")
API_KEY = env_manager.get("ENV_API_KEY")
AI_MODEL = env_manager.get("ENV_AI_MODEL")

# Check if the API key is loaded
if not API_KEY:
    print("\u274C Error: The API key was not loaded from the .env file.")
    exit()
else:
    print("\u2705 API key loaded successfully!")

# Initialize AiClient
ai_client = AiClient(API_KEY, BASE_URL, AI_MODEL)

# Load voices from JSON file
with open('voices.json', 'r') as file:
    voices_data = json.load(file)

# Display available voices
print("\n🔊 Choose a voice:")
for idx, voice in enumerate(voices_data):
    print(f"{idx + 1}. {voice['name']} from {voice['country']}")

# Ask the user to choose a voice
voice_choice = int(input("Enter the number of the voice you want to use: ")) - 1
chosen_voice = voices_data[voice_choice]
name = chosen_voice['name']
country = chosen_voice['country']
short_name = chosen_voice['shortName']

print(f"✅ You selected the voice: {name} from {country}")

# Ask the user for their IELTS level and theme
level_chosen = input("\U0001F3AF What IELTS level are you aiming for? B1, B2, or C1: ")
theme_chosen = input("\U0001F3A8 What topic would you like to talk about? ")
user_speech = input("\U0001F3A4 Do you want to write or speak? ")

# Initialize SpeechManager for text-to-speech and speech-to-text
speech_manager = SpeechManager()

# Initialize IELTSManager to handle questions and interview
ielts_manager = IELTSManager(level_chosen, theme_chosen, name, country)

# Generate interview questions by passing the voice name and country
question_list = ielts_manager.generate_ordered_ielts_questions(theme_chosen, name, country)
discussion = [
    {
        "role": "system",
        "content": f"""You are an IELTS examiner helping a student prepare for their IELTS speaking exam.
The goal is to achieve a {level_chosen} level on the topic "{theme_chosen}".

🧠 Your rules:
- Evaluate the conversation solely based on your questions and the user's answers.
- Use the IELTS scoring scale from 1 (no English) to 9 (C2).
- Provide a score for each criterion (Fluency and Coherence, Lexical Resource, Grammatical Range and Accuracy, Pronunciation).
- Return a global band score and a brief feedback summary."""
    }
]

question_index = 0

# Main function to ask questions and handle user responses
while question_index < len(question_list):
    current_part, current_question, duration = question_list[question_index]

    if current_part == "Prep":
        print(f"\n⏳ {current_question}")
        speech_manager.say_and_play(current_question, short_name)  # Pass the voice here
        time.sleep(duration)
        question_index += 1
        continue

    print(f"\n🗂️ {current_part} — {current_question}")
    speech_manager.say_and_play(current_question, short_name)  # Pass the voice here

    discussion.append({"role": "assistant", "content": current_question})

    if user_speech == "write":
        message = input("- ")
    else:
        print("🎙️ Speak now...")
        recording = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
        sd.wait()
        write("user_speech.wav", 44100, recording)
        result = whisper.load_model("base").transcribe("user_speech.wav")
        transcription = result["text"]
        print("📝 You said:", transcription)
        message = transcription

    if message.strip().upper() == "!STOP":
        print("👋 Goodbye!")
        break

    # Clean up the message before adding to the discussion
    clean_response = re.sub(r"\([^)]*\)|\*[^*]*\*", "", message).strip()
    discussion.append({"role": "user", "content": clean_response})

    question_index += 1

    # Encouraging messages and transition between parts
    if current_part == "Part 1" and question_index == 4:
        print("\n🎯 Good answers so far! Let's move to Part 2.")
        speech_manager.say_and_play("Good answers so far! Let's move to Part 2.", short_name)
    elif current_part == "Part 2":
        print("\n🚀 Great job in Part 2! Now, let's move to Part 3.")
        speech_manager.say_and_play("Great job in Part 2! Now, let's move to Part 3.", short_name)
    elif current_part == "Part 3" and question_index == 9:
        print("\n🎉 Well done! Now, let's proceed to the evaluation.")
        speech_manager.say_and_play("Well done! Now, let's proceed to the evaluation.", short_name)

# Evaluate the user's performance using IELTSManager's evaluate method
test_grade = ai_client.evaluate(discussion)

print(test_grade)
