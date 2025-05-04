# bot/handlers/burnout.py

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.main_keyboard import main_menu
from bot.services.openai_assistant import ask_mia

router = Router(name="burnout")


class BurnoutTest(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()


questions = [
    "1️⃣ Как часто ты чувствуешь усталость, даже если выспался(ась)?",
    "2️⃣ Замечаешь ли у себя снижение интереса к тому, что раньше радовало?",
    "3️⃣ Трудно ли тебе сосредоточиться на задачах?",
    "4️⃣ Чувствуешь ли ты эмоциональное выгорание?",
    "5️⃣ Есть ли ощущение, что ты на пределе своих возможностей?"
]

answers = []


@router.message(F.text.lower() == "🔥 выгорание")
async def start_burnout_test(message: types.Message, state: FSMContext):
    global answers
    answers = []
    await message.answer(questions[0])
    await state.set_state(BurnoutTest.q1)


@router.message(BurnoutTest.q1)
async def burnout_q1(message: types.Message, state: FSMContext):
    answers.append(message.text)
    await message.answer(questions[1])
    await state.set_state(BurnoutTest.q2)


@router.message(BurnoutTest.q2)
async def burnout_q2(message: types.Message, state: FSMContext):
    answers.append(message.text)
    await message.answer(questions[2])
    await state.set_state(BurnoutTest.q3)


@router.message(BurnoutTest.q3)
async def burnout_q3(message: types.Message, state: FSMContext):
    answers.append(message.text)
    await message.answer(questions[3])
    await state.set_state(BurnoutTest.q4)


@router.message(BurnoutTest.q4)
async def burnout_q4(message: types.Message, state: FSMContext):
    answers.append(message.text)
    await message.answer(questions[4])
    await state.set_state(BurnoutTest.q5)


@router.message(BurnoutTest.q5)
async def burnout_q5(message: types.Message, state: FSMContext):
    answers.append(message.text)
    await state.clear()

    combined_answers = "\n".join([f"{i + 1}. {q}\nОтвет: {a}" for i, (q, a) in enumerate(zip(questions, answers))])
    prompt = f"""Пользователь прошел мини-тест на эмоциональное выгорание. Вот его ответы:

{combined_answers}

На основе этих данных составь мягкий психологический портрет. Объясни, как выгорание может проявляться. Дай понятные, поддерживающие рекомендации, как восстановить силы и снизить стресс. Ты — заботливая психолог Мия, говори человечно."""

    response = await ask_mia(prompt)
    await message.answer(response, reply_markup=main_menu())
