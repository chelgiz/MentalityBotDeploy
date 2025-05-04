from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards.main_keyboard import main_menu

router = Router()

@router.message(F.text.lower().contains("sos"))
async def sos_help(message: Message):
    await message.answer(
        "🚨 Режим SOS активирован.\n"
        "Попробуй одно из:\n"
        "— Сделай глубокий вдох и медленный выдох\n"
        "— Посмотри по сторонам и назови 5 предметов\n"
        "— Напиши, что тебя беспокоит — я рядом\n"
        "\nЕсли ситуация критическая:\n📞 Обратись по номеру 112 или в ближайший кризисный центр"
    )
    await message.answer("⬅️ Возвращаемся в главное меню.", reply_markup=main_menu())
