import json
import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play
import whisper as wp

class VoiceManager:
    def __init__(self, voices_file="voices.json"):
        # Charger le fichier voices.json
        with open(voices_file, 'r', encoding='utf-8') as file:
            self.voices_data = json.load(file)

        # ✅ Alias pour compatibilité avec le reste de l'app
        self.voices = self.voices_data

    def transcribe_audio(self, audio_path):
        """Fonction pour transcrire un fichier audio en texte"""
        result = wp.load_model("base").transcribe(audio_path)
        return result["text"]

    async def speak(self, text, voice):
        """Utilise EdgeTTS pour lire le texte à voix haute."""
        communicate = edge_tts.Communicate(text, voice=voice)
        await communicate.save("bot_speech.mp3")
        audio = AudioSegment.from_file("bot_speech.mp3", format="mp3")
        play(audio)

    def say_and_play(self, text, voice):
        """Fonction synchrone pour lire le texte."""
        asyncio.run(self.speak(text, voice))

    def select_voice(self):
        """Permet à l'utilisateur de sélectionner une voix à partir du fichier voices.json"""
        print("Choisissez une voix parmi les options suivantes :")
        for idx, voice in enumerate(self.voices_data, 1):
            print(f"{idx}. {voice['name']} ({voice['country']}) - {voice['gender']}")

        # Demander à l'utilisateur de choisir une voix
        try:
            choice = int(input("Entrez le numéro de la voix que vous voulez utiliser: "))
            if choice < 1 or choice > len(self.voices_data):
                print("Choix invalide.")
                return self.select_voice()
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            return self.select_voice()

        # Retourner le shortName de la voix sélectionnée
        selected_voice = self.voices_data[choice - 1]['shortName']
        print(f"✅ Vous avez sélectionné la voix: {self.voices_data[choice - 1]['name']}")
        return selected_voice
