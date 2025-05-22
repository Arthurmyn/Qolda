import tkinter as tk
import threading
import whisper
import pyaudio
import wave
import time
from text_to_sign import convert_text_to_gestures
from gesture_output import save_gestures_to_json

model = whisper.load_model("small")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "temp_chunk.wav"

is_listening = False

def record_and_transcribe_loop():
    global is_listening
    p = pyaudio.PyAudio()

    while is_listening:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if not is_listening:
                break
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        # Сохраняем кусок
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # Распознаём и обновляем интерфейс
        status_label.config(text="🔎 Распознаю...")
        result = model.transcribe(WAVE_OUTPUT_FILENAME, language="ru")
        text = result["text"]

        gestures = convert_text_to_gestures(text)
        save_gestures_to_json(gestures)

        output_text.insert(tk.END, f"🗣️ {text.strip()}\n")
        output_text.see(tk.END)  # автоскролл
        status_label.config(text="🎤 В прямом эфире...")

        time.sleep(0.2)

    p.terminate()
    status_label.config(text="⏹️ Остановлено.")

def start_stream():
    global is_listening
    if not is_listening:
        is_listening = True
        threading.Thread(target=record_and_transcribe_loop).start()
        status_label.config(text="🎤 В прямом эфире...")

def stop_stream():
    global is_listening
    is_listening = False

# GUI
root = tk.Tk()
root.title("Qolda Live")

start_button = tk.Button(root, text="🎙️ Старт прямого эфира", command=start_stream, font=("Arial", 12))
start_button.pack(pady=5)

stop_button = tk.Button(root, text="⏹️ Стоп", command=stop_stream, font=("Arial", 12))
stop_button.pack(pady=5)

status_label = tk.Label(root, text="🟢 Готов к запуску", font=("Arial", 11))
status_label.pack()

output_text = tk.Text(root, height=15, width=60, font=("Arial", 10))
output_text.pack(pady=10)

root.mainloop()
