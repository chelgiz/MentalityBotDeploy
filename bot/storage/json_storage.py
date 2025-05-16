
import json
import os

DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

def _get_user_file(user_id: int):
    return os.path.join(DATA_DIR, f"{user_id}_history.json")

def save_user_message(user_id: int, role: str, content: str):
    path = _get_user_file(user_id)
    history = load_user_history(user_id)
    history.append({"role": role, "content": content})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_user_history(user_id: int):
    path = _get_user_file(user_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
