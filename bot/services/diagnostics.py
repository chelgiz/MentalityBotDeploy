from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards.main_keyboard import main_menu

router = Router()

@router.message(Command("diagnostics"))
@router.message(lambda msg: msg.text == "🔍 Пройти диагностику")
async def start_diagnostics(message: types.Message):
    text = (
        "🧠 Добро пожаловать в раздел диагностики!"
        "Здесь ты можешь пройти различные психологические тесты и спецопросы, "
        "чтобы лучше понять своё внутреннее состояние. Выбирай нужный пункт из меню ниже ⬇️"
    )
    await message.answer(text, reply_markup=main_menu())
