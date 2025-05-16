# bot/handlers/mfi20.py

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.main_keyboard import main_menu
from bot.services.openai_assistant import ask_mia

router = Router()

class MFI20(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()

questions = {
    "Q1": "Как часто ты чувствуешь физическую усталость?",
    "Q2": "Как часто у тебя нет энергии для выполнения обычных задач?",
    "Q3": "Как часто ты испытываешь эмоциональное истощение?",
    "Q4": "Как часто ты теряешь мотивацию даже к важным делам?",
}

@router.message(F.text == "⚡ Астения")
async def start_mfi(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(MFI20.Q1)
    await state.update_data(score=0)
    await message.answer("Мы начнём тест на астению. Отвечай честно по шкале:\n\n"
                         "0 — никогда\n1 — редко\n2 — иногда\n3 — часто\n4 — всегда\n\n"
                         f"{questions['Q1']}")

@router.message(MFI20.Q1)
async def mfi_q1(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) not in range(5):
        return await message.answer("Пожалуйста, введи число от 0 до 4.")
    await state.update_data(score=int(message.text))
    await state.set_state(MFI20.Q2)
    await message.answer(questions["Q2"])

@router.message(MFI20.Q2)
async def mfi_q2(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) not in range(5):
        return await message.answer("Пожалуйста, введи число от 0 до 4.")
    data = await state.get_data()
    score = data["score"] + int(message.text)
    await state.update_data(score=score)
    await state.set_state(MFI20.Q3)
    await message.answer(questions["Q3"])

@router.message(MFI20.Q3)
async def mfi_q3(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) not in range(5):
        return await message.answer("Пожалуйста, введи число от 0 до 4.")
    data = await state.get_data()
    score = data["score"] + int(message.text)
    await state.update_data(score=score)
    await state.set_state(MFI20.Q4)
    await message.answer(questions["Q4"])

@router.message(MFI20.Q4)
async def mfi_q4(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) not in range(5):
        return await message.answer("Пожалуйста, введи число от 0 до 4.")

    data = await state.get_data()
    total_score = data["score"] + int(message.text)
    await state.clear()

    await message.answer(f"🔎 Тест завершён.\nОбщий балл: <b>{total_score}</b> из 16.\nПодключаю Мию...")

    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"

    prompt = (
        f"Пользователь прошёл короткий тест MFI-20 на астению (усталость). "
        f"Общий балл: {total_score} из 16.\n"
        f"Проанализируй результат и сделай вывод, есть ли признаки астении. "
        f"Объясни на доступном языке, как это может сказываться на состоянии человека, "
        f"и предложи конкретные шаги по восстановлению и снижению утомляемости."
    )

    response = await ask_mia(user_id, user_name, prompt)
    await message.answer(response, reply_markup=main_menu())
