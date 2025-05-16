# bot/handlers/spilberger.py

from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.services.openai_assistant import ask_mia
from bot.keyboards.main_keyboard import main_menu

router = Router()


class SpilbergerTest(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()


questions = [
    "1️⃣ Ты часто ощущаешь внутреннее напряжение или тревогу без причины?",
    "2️⃣ Как часто ты испытываешь беспокойство перед важными событиями?",
    "3️⃣ Бывает ли, что ты не можешь расслабиться даже в спокойной обстановке?",
    "4️⃣ Ты легко теряешь контроль над эмоциями?"
]


@router.message(F.text == "📊 Спилбергер")
async def spilberger_start(message: types.Message, state: FSMContext):
    await state.set_state(SpilbergerTest.q1)
    await message.answer("📊 Тест Спилбергера оценивает уровень тревожности.\n\nОцени каждый вопрос по шкале от 0 до 3:\n0 — никогда\n1 — иногда\n2 — часто\n3 — почти всегда\n\n" + questions[0])


@router.message(SpilbergerTest.q1)
async def spilberger_q1(message: types.Message, state: FSMContext):
    await state.update_data(q1=message.text)
    await state.set_state(SpilbergerTest.q2)
    await message.answer(questions[1])


@router.message(SpilbergerTest.q2)
async def spilberger_q2(message: types.Message, state: FSMContext):
    await state.update_data(q2=message.text)
    await state.set_state(SpilbergerTest.q3)
    await message.answer(questions[2])


@router.message(SpilbergerTest.q3)
async def spilberger_q3(message: types.Message, state: FSMContext):
    await state.update_data(q3=message.text)
    await state.set_state(SpilbergerTest.q4)
    await message.answer(questions[3])


@router.message(SpilbergerTest.q4)
async def spilberger_q4(message: types.Message, state: FSMContext):
    await state.update_data(q4=message.text)
    data = await state.get_data()
    await state.clear()

    try:
        scores = [int(data[f'q{i}']) for i in range(1, 5)]
        total = sum(scores)
    except ValueError:
        await message.answer("Пожалуйста, используй только цифры от 0 до 3 для ответа.")
        return

    summary = f"Результаты теста Спилбергера: {total} баллов.\n\n"
    if total <= 4:
        summary += "🟢 Низкий уровень тревожности. Всё под контролем."
    elif 5 <= total <= 9:
        summary += "🟡 Умеренная тревожность. Есть поводы для внимания."
    elif 10 <= total <= 14:
        summary += "🟠 Высокий уровень тревожности."
    else:
        summary += "🔴 Очень высокая тревожность. Рекомендуется психотерапия."

    user_name = message.from_user.first_name or "друг"
    user_id = message.from_user.id
    response = await ask_mia(user_id, user_name, f"{summary}\n\nМия, пожалуйста, опиши тревожный профиль пользователя и подскажи, как ему помочь мягко и с заботой.")

    await message.answer(f"<b>{summary}</b>\n\n{response}", reply_markup=main_menu())
