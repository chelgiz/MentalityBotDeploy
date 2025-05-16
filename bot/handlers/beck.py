# bot/handlers/beck.py

from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.services.openai_assistant import ask_mia
from bot.keyboards.main_keyboard import main_menu

router = Router()


class BeckTest(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()


questions = [
    "1️⃣ Как часто ты чувствуешь усталость или апатию?",
    "2️⃣ Тебе часто трудно найти мотивацию что-то делать?",
    "3️⃣ Бывают ли у тебя периоды, когда ты теряешь интерес к вещам, которые раньше радовали?",
    "4️⃣ Как часто у тебя бывают грустные или тревожные мысли?"
]


@router.message(F.text == "📘 Бек")
async def beck_start(message: types.Message, state: FSMContext):
    await state.set_state(BeckTest.q1)
    await message.answer("📘 Тест Бека — один из самых известных тестов на депрессию.\n\nОцени каждый вопрос по шкале от 0 до 3:\n0 — никогда\n1 — иногда\n2 — часто\n3 — почти всегда\n\n" + questions[0])


@router.message(BeckTest.q1)
async def beck_q1(message: types.Message, state: FSMContext):
    await state.update_data(q1=message.text)
    await state.set_state(BeckTest.q2)
    await message.answer(questions[1])


@router.message(BeckTest.q2)
async def beck_q2(message: types.Message, state: FSMContext):
    await state.update_data(q2=message.text)
    await state.set_state(BeckTest.q3)
    await message.answer(questions[2])


@router.message(BeckTest.q3)
async def beck_q3(message: types.Message, state: FSMContext):
    await state.update_data(q3=message.text)
    await state.set_state(BeckTest.q4)
    await message.answer(questions[3])


@router.message(BeckTest.q4)
async def beck_q4(message: types.Message, state: FSMContext):
    await state.update_data(q4=message.text)
    data = await state.get_data()
    await state.clear()

    try:
        scores = [int(data[f'q{i}']) for i in range(1, 5)]
        total = sum(scores)
    except ValueError:
        await message.answer("Кажется, ты ввёл что-то не то. Пожалуйста, проходи тест, используя цифры от 0 до 3.")
        return

    summary = f"Результаты теста Бека: {total} баллов.\n\n"
    if total <= 4:
        summary += "🟢 Вероятно, признаков депрессии нет или они минимальны."
    elif 5 <= total <= 9:
        summary += "🟡 Лёгкая степень депрессивного состояния."
    elif 10 <= total <= 14:
        summary += "🟠 Средняя степень депрессии."
    else:
        summary += "🔴 Высокий уровень депрессии. Рекомендуется обратиться к специалисту."

    user_name = message.from_user.first_name or "друг"
    user_id = message.from_user.id
    response = await ask_mia(user_id, user_name, f"{summary}\n\nДай, пожалуйста, развёрнутый психологический портрет и рекомендации.")

    await message.answer(f"<b>{summary}</b>\n\n{response}", reply_markup=main_menu())
