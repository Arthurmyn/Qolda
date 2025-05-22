import json

def save_gestures_to_json(gestures, filename="gestures.json"):
    data = {"gestures": gestures}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Жесты сохранены в {filename}")
