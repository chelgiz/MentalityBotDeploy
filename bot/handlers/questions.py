from aiogram import Router, types
from aiogram.filters import Command
from bot.services.openai_assistant import ask_mia

router = Router()

@router.message(Command("start_chat"))
@router.message(lambda msg: msg.text == "🧠 Задать вопрос Мии")
async def handle_question(message: types.Message):
    await message.answer("Что бы ты хотел спросить у Мии? Напиши свой вопрос.")

@router.message()
async def handle_free_text(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"
    user_message = message.text

    try:
        answer = await ask_mia(user_id, user_name, user_message)
        await message.answer(answer)
    except Exception as e:
        await message.answer("Мия временно недоступна. Попробуй ещё раз чуть позже 🙏")
