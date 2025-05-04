from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards.main_keyboard import main_menu

router = Router()

@router.message(F.text.lower().contains("практики"))
async def relief_practices(message: Message):
    await message.answer(
        "🧘 Практики, которые ты можешь попробовать:\n\n"
        "1. Дыхание 4-7-8: вдохни на 4 счёта, задержи на 7, выдохни на 8\n"
        "2. Запиши 3 вещи, за которые ты благодарен\n"
        "3. Прогулка на 15 минут без телефона\n"
        "4. Музыка с альфа-ритмами\n"
        "5. Посмотри на небо, деревья или воду — минимум 3 минуты"
    )
    await message.answer("⬅️ Возвращаемся в главное меню.", reply_markup=main_menu())
