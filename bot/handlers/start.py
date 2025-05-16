from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.main_keyboard import main_menu

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Я Мия — твой эмпатичный помощник 🧠\n"
        "Готова поддержать тебя. Выбери, с чего начнём:",
        reply_markup=main_menu()
    )
