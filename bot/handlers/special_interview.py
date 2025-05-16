from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.services.openai_assistant import ask_mia_special

router = Router()

class SpecialInterview(StatesGroup):
    waiting_for_answer = State()

@router.message(F.text == "🧠 Психологическая карта")
async def start_special_interview(message: types.Message, state: FSMContext):
    await state.set_state(SpecialInterview.waiting_for_answer)
    user_name = message.from_user.first_name or "друг"
    greeting = (
"Привет. Давай начнём. Я задам тебе серию простых, но важных вопросов, чтобы лучше понять тебя."
        "Отвечай свободно, как чувствуешь. Первый вопрос:"
        "👉 Расскажи о моменте из детства, который тебе особенно запомнился."
    )
    await message.answer(greeting)

@router.message(SpecialInterview.waiting_for_answer)
async def handle_special_answer(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"
    user_message = message.text

    response = await ask_mia_special(user_id, user_name, user_message)
    await message.answer(response)