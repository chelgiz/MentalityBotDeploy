import json
import os
from datetime import datetime

DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

def save_user_result(user_id: int, category: str, result: dict):
    file_path = os.path.join(DATA_DIR, f"{user_id}_{category}.json")
    data = {"timestamp": datetime.now().isoformat(), "result": result}
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

def load_user_results(user_id: int, category: str) -> list:
    file_path = os.path.join(DATA_DIR, f"{user_id}_{category}.json")
    if not os.path.exists(file_path):
        return []
    with open(file_path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]
