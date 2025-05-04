# bot/handlers/mfi20.py

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.main_keyboard import main_menu
from bot.services.openai_assistant import ask_mia

router = Router(name="mfi20")

class MFI20(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()

questions = [
    "1️⃣ Часто ли ты чувствуешь усталость, даже не начиная работать?",
    "2️⃣ Насколько сложно тебе поддерживать концентрацию в течение дня?",
    "3️⃣ Чувствуешь ли ты себя истощенным(ой) эмоционально или физически?",
    "4️⃣ Удается ли тебе восстановиться после обычного отдыха?"
]

answers = []

@router.message(F.text.lower() == "⚡ астения")
async def start_mfi20(message: types.Message, state: FSMContext):
    global answers
    answers = []
    await message.answer(questions[0])
    await state.set_state(MFI20.q1)

@router.message(MFI20.q1)
async def mfi_q1(message: types.Message, state: FSMContext):
    answers.append(message.text)
    await message.answer(questions[1])
    await state.set_state(MFI20.q2)

@router.message(MFI20.q2)
async def mfi_q2(message: types.Message, state: FSMContext):
    answers.append(message.text)
    await message.answer(questions[2])
    await state.set_state(MFI20.q3)

@router.message(MFI20.q3)
async def mfi_q3(message: types.Message, state: FSMContext):
    answers.append(message.text)
    await message.answer(questions[3])
    await state.set_state(MFI20.q4)

@router.message(MFI20.q4)
async def mfi_q4(message: types.Message, state: FSMContext):
    answers.append(message.text)
    await state.clear()

    summary = "\n".join([f"{i+1}. {q}\nОтвет: {a}" for i, (q, a) in enumerate(zip(questions, answers))])
    prompt = f"""Пользователь прошёл мини-версию теста MFI-20 на астению (утомление). Вот его ответы:

{summary}

Составь развернутый, сочувствующий психологический портрет на основе этих ответов. Дай понятные рекомендации, как справляться с астенией, усталостью, снижением жизненных сил. Пиши от имени Мии — тёплого эмпатичного помощника."""

    response = await ask_mia(prompt)
    await message.answer(response, reply_markup=main_menu())
