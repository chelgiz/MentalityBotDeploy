import os
import matplotlib.pyplot as plt
from datetime import datetime
from bot.storage.json_storage import load_user_results

def generate_checkin_plot(user_id: int) -> str | None:
    data = load_user_results(user_id, "checkin")
    if not data:
        return None

    timestamps = [datetime.fromisoformat(entry["timestamp"]) for entry in data]
    mood = [entry["result"]["mood"] for entry in data]
    energy = [entry["result"]["energy"] for entry in data]
    motivation = [entry["result"]["motivation"] for entry in data]

    plt.figure(figsize=(8, 4))
    plt.plot(timestamps, mood, label="Настроение")
    plt.plot(timestamps, energy, label="Энергия")
    plt.plot(timestamps, motivation, label="Мотивация")
    plt.legend()
    plt.title("🧭 Динамика состояния")
    plt.xlabel("Дата")
    plt.ylabel("Оценка")
    plt.tight_layout()

    os.makedirs("user_data/charts", exist_ok=True)
    path = f"user_data/charts/{user_id}_chart.png"
    plt.savefig(path)
    plt.close()
    return path
