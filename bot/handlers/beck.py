from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards.main_keyboard import main_menu
from bot.services.openai_assistant import ask_mia

router = Router()

class Beck(StatesGroup):
    q0 = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()

questions = [
    "Вопрос 1 Бека: Я чувствую себя подавленным...",
    "Вопрос 2: Я чувствую себя бесполезным...",
    "Вопрос 3: Я испытываю трудности с принятием решений...",
    "Вопрос 4: Я чувствую усталость или утомляемость...",
    "Вопрос 5: Я чувствую тревогу или напряжение..."
]

options = ["0 — Нет", "1 — Немного", "2 — Умеренно", "3 — Сильно"]

states = [Beck.q0, Beck.q1, Beck.q2, Beck.q3, Beck.q4]

@router.message(F.text == "📘 Бек")
async def start_beck(message: Message, state: FSMContext):
    await state.set_state(Beck.q0)
    await state.set_data({"answers": []})
    await message.answer("📋 Начинаем тест Бека. Отвечай от 0 до 3.")
    await message.answer(questions[0], reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in options],
        resize_keyboard=True,
        one_time_keyboard=True
    ))

@router.message(Beck.q0)
@router.message(Beck.q1)
@router.message(Beck.q2)
@router.message(Beck.q3)
@router.message(Beck.q4)
async def handle_beck(message: Message, state: FSMContext):
    data = await state.get_data()
    answers = data.get("answers", [])

    try:
        score = int(message.text.split("—")[0].strip())
        answers.append(score)
    except:
        await message.answer("Пожалуйста, выбери вариант из списка.")
        return

    if len(answers) < len(questions):
        await state.set_data({"answers": answers})
        await state.set_state(states[len(answers)])
        await message.answer(questions[len(answers)], reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=opt)] for opt in options],
            resize_keyboard=True,
            one_time_keyboard=True
        ))
    else:
        total = sum(answers)
        await state.clear()
        await message.answer("✅ Тест завершён. Составляю психологический портрет...", reply_markup=main_menu())

        prompt = f"""Я прошёл тест Бека на уровень депрессии. Мой итоговый балл: {total} из 15.
Поясни мне, пожалуйста, что это может значить, какой это уровень и какие шаги мне стоит предпринять.
Предложи поддержку от Мии."""

        response = await ask_mia(prompt)
        await message.answer(response)
