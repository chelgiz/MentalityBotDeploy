from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Пройти диагностику"), KeyboardButton(text="🧠 Задать вопрос Мии")],
            [KeyboardButton(text="🧠 Психологическая карта"), KeyboardButton(text="📈 Прогресс")],
            [KeyboardButton(text="✅ Чек-ин"), KeyboardButton(text="🌿 Практики")],
            [KeyboardButton(text="🔥 Выгорание"), KeyboardButton(text="📘 Бек"), KeyboardButton(text="📊 Спилбергер")],
            [KeyboardButton(text="⚡ Астения"), KeyboardButton(text="🧾 PHQ-9"), KeyboardButton(text="🆘 SOS-помощь")]
        ],
        resize_keyboard=True
    )
