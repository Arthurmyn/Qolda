from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print("❌ Ошибка при расшифровке:", e)
        return ""

if __name__ == "__main__":
    path = "audio_samples/Qolda 2.m4a"
    result = transcribe_audio(path)
    print("📜 Распознанный текст:\n", result)
