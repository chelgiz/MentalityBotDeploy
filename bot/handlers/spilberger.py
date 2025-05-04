from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.main_keyboard import main_menu
from bot.services.openai_assistant import ask_mia

router = Router()

class SpilbergerStates(StatesGroup):
    awaiting_answer = State()

questions = [
    "1. Я чувствую себя спокойным.",
    "2. Я напряжен.",
    "3. Я встревожен.",
    "4. Я чувствую себя уверенно.",
    "5. Я чувствую себя испуганным.",
    "6. Я чувствую себя комфортно.",
    "7. Я чувствую раздражение.",
    "8. Я испытываю тревогу.",
    "9. Я легко расстраиваюсь.",
    "10. Я расслаблен."
]

score_map = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4
}

user_answers = {}

@router.message(lambda msg: msg.text == "📊 Спилбергер")
async def start_spilberger(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id] = []
    await state.set_state(SpilbergerStates.awaiting_answer)
    await message.answer(
        "Ответь на утверждение по шкале от 1 до 4:\n1 — совсем не так\n4 — совершенно верно\n\n" + questions[0],
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=str(i)) for i in range(1, 5)]],
            resize_keyboard=True
        )
    )

@router.message(SpilbergerStates.awaiting_answer)
async def handle_spilberger(message: types.Message, state: FSMContext):
    if message.text not in score_map:
        await message.answer("Пожалуйста, выбери ответ от 1 до 4.")
        return

    user_id = message.from_user.id
    user_answers[user_id].append(score_map[message.text])
    question_index = len(user_answers[user_id])

    if question_index < len(questions):
        await message.answer(questions[question_index])
    else:
        total_score = sum(user_answers[user_id])
        del user_answers[user_id]
        await state.clear()

        prompt = (
            f"Пользователь прошёл тест Спилбергера (оценка тревожности) и набрал {total_score} баллов из 40.\n"
            f"Составь краткий психологический портрет пользователя, оцени уровень тревожности и мягко предложи рекомендации, "
            f"как можно снизить тревогу, если она присутствует. Говори дружелюбно и поддерживающе."
        )
        response = await ask_mia(prompt)

        await message.answer(f"Тест завершён. Вот ответ от Мии:\n\n{response}", reply_markup=main_menu())
