from aiogram import Router, F
from aiogram.types import Message
from bot.services.diagnostic_summary import generate_diagnostic_summary
from bot.keyboards.main_keyboard import main_menu

router = Router()

# 🔧 Временно: моковые данные, пока не подключено хранилище
mock_results = {
    "phq9": 14,
    "beck": 23,
    "spilberger_state": 41,
    "spilberger_trait": 48,
    "mfi20": 57,
    "burnout_ee": 28,
    "burnout_dp": 16,
    "burnout_pa": 29
}

@router.message(F.text.lower() == "мой психологический анализ")
async def send_summary(message: Message):
    await message.answer("🧠 Анализирую твоё психоэмоциональное состояние...")
    try:
        summary = await generate_diagnostic_summary(mock_results)
        await message.answer(summary, reply_markup=main_menu())
    except Exception as e:
        print("OpenAI error:", e)
        await message.answer(
            "🚫 Произошла ошибка при анализе. Попробуй ещё раз позже.",
            reply_markup=main_menu()
        )
