import whisper

model = whisper.load_model("small")

file_path = "audio_samples/Sample.m4a"

result = model.transcribe(file_path, language="ru")

print("Распознанный текст:\n", result["text"])
