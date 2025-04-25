import asyncio
import whisper
import edge_tts
from pydub import AudioSegment
from pydub.playback import play

class SpeechManager:
    def __init__(self):
        # Charger le modèle Whisper
        self.whisper_model = whisper.load_model("base")

    def transcribe_audio(self, audio_path):
        """Transcrit un fichier audio en texte."""
        result = self.whisper_model.transcribe(audio_path)
        return result["text"]

    async def speak(self, text, voice):
        """Utilise EdgeTTS pour lire le texte à voix haute."""
        communicate = edge_tts.Communicate(text, voice=voice)
        await communicate.save("output.mp3")
        audio = AudioSegment.from_file("output.mp3", format="mp3")
        play(audio)

    def say_and_play(self, text, voice):
        """Fonction synchrone pour lire le texte."""
        asyncio.run(self.speak(text, voice))
