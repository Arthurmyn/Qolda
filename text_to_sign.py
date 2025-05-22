# text_to_sign.py

# Мини-словарь жестов
gesture_dict = {
    "привет": "wave",
    "как": "how",
    "дела": "ok",
    "спасибо": "thank_you",
    "да": "yes",
    "нет": "no",
    "пока": "bye"
}

def convert_text_to_gestures(text):
    words = text.lower().split()
    gestures = []

    for word in words:
        if word in gesture_dict:
            gestures.append(gesture_dict[word])
        else:
            gestures.append("idle")  # запасной жест
    return gestures
