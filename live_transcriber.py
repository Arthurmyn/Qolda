import tkinter as tk
import threading
import whisper
import pyaudio
import wave
from text_to_sign import convert_text_to_gestures
from gesture_output import save_gestures_to_json

model = whisper.load_model("tiny")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10  # макс. длина, можно прервать раньше
WAVE_OUTPUT_FILENAME = "temp_audio.wav"

recording = False  # глобальный флаг

def record_audio():
    global recording
    recording = True

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    status_label.config(text="🎙️ Идёт запись...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        if not recording:
            break
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    status_label.config(text="🧠 Распознаю речь...")
    result = model.transcribe(WAVE_OUTPUT_FILENAME, language="ru")
    text = result["text"]
    gestures = convert_text_to_gestures(text)
    save_gestures_to_json(gestures)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"📜 Текст: {text}\n🧠 Жесты: {gestures}")
    status_label.config(text="✅ Готово!")

def start_recording():
    thread = threading.Thread(target=record_audio)
    thread.start()

def stop_recording():
    global recording
    recording = False
    status_label.config(text="⏹️ Остановлено пользователем")

# GUI setup
root = tk.Tk()
root.title("Qolda: Речь → Жесты")

start_button = tk.Button(root, text="🎙️ Начать запись", command=start_recording, font=("Arial", 14))
start_button.pack(pady=5)

stop_button = tk.Button(root, text="⏹️ Остановить запись", command=stop_recording, font=("Arial", 14))
stop_button.pack(pady=5)

status_label = tk.Label(root, text="Готов к записи", font=("Arial", 12))
status_label.pack()

output_text = tk.Text(root, height=10, width=60, font=("Arial", 10))
output_text.pack(pady=10)

root.mainloop()
