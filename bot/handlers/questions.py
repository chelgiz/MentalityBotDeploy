from aiogram import Router, types
from aiogram.types import Message
from bot.services.openai_assistant import ask_mia

router = Router()


@router.message()
async def handle_question(message: Message):
    user_text = message.text
    await message.answer("<i>Мия думает...</i> 🧠", parse_mode="HTML")

    answer = ask_mia(user_text)  # <— теперь без await
    await message.answer(answer)
