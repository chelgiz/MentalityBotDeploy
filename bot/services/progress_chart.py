from datetime import datetime
import os
import matplotlib.pyplot as plt
import json


def generate_checkin_plot(user_id: int) -> str:
    """Генерация графика прогресса чек-инов"""
    file_path = f"user_data/{user_id}_checkin.json"
    if not os.path.exists(file_path):
        raise FileNotFoundError("Нет данных чек-инов для этого пользователя.")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    timestamps = []
    values = []

    for entry in data:
        try:
            # Только если дата в ISO-формате
            timestamp = datetime.fromisoformat(entry["timestamp"])
            timestamps.append(timestamp)
            values.append(entry["value"])
        except Exception:
            continue  # Пропускаем записи с неправильными датами

    if not timestamps or not values:
        raise ValueError("Недостаточно корректных данных для построения графика.")

    # Сортировка по дате
    sorted_data = sorted(zip(timestamps, values), key=lambda x: x[0])
    dates, sorted_values = zip(*sorted_data)

    # Построение графика
    plt.figure()
    plt.plot(dates, sorted_values, marker='o')
    plt.xlabel("Дата")
    plt.ylabel("Оценка состояния")
    plt.title("Прогресс чек-инов")
    plt.grid(True)

    image_path = f"user_data/{user_id}_progress.png"
    plt.savefig(image_path)
    plt.close()

    return image_path
