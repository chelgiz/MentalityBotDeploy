from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.services.openai_assistant import ask_mia
from aiogram.filters import Command

router = Router()

class BurnoutTest(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()

# Старт команды
@router.message(F.text == "🔥 Выгорание")
async def start_burnout(message: types.Message, state: FSMContext):
    await message.answer("🧪 Тест на выгорание. Отвечай честно.\n\n1️⃣ Как часто ты чувствуешь себя истощённым после работы?")
    await state.set_state(BurnoutTest.Q1)

@router.message(BurnoutTest.Q1)
async def burnout_q1(message: types.Message, state: FSMContext):
    await state.update_data(q1=message.text)
    await message.answer("2️⃣ Снижается ли у тебя интерес или мотивация к тому, что раньше вдохновляло?")
    await state.set_state(BurnoutTest.Q2)

@router.message(BurnoutTest.Q2)
async def burnout_q2(message: types.Message, state: FSMContext):
    await state.update_data(q2=message.text)
    await message.answer("3️⃣ Чувствуешь ли ты безразличие или цинизм по отношению к работе?")
    await state.set_state(BurnoutTest.Q3)

@router.message(BurnoutTest.Q3)
async def burnout_q3(message: types.Message, state: FSMContext):
    await state.update_data(q3=message.text)
    await message.answer("4️⃣ Есть ли у тебя физические симптомы (бессонница, головные боли, усталость)?")
    await state.set_state(BurnoutTest.Q4)

@router.message(BurnoutTest.Q4)
async def burnout_q4(message: types.Message, state: FSMContext):
    await state.update_data(q4=message.text)
    await message.answer("5️⃣ Испытываешь ли ты чувство беспомощности или отчаяния?")
    await state.set_state(BurnoutTest.Q5)

@router.message(BurnoutTest.Q5)
async def burnout_q5(message: types.Message, state: FSMContext):
    await state.update_data(q5=message.text)
    data = await state.get_data()
    await state.clear()

    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"

    prompt = (
        f"Пользователь прошел тест на выгорание.\n"
        f"Вот его ответы:\n"
        f"1. {data['q1']}\n"
        f"2. {data['q2']}\n"
        f"3. {data['q3']}\n"
        f"4. {data['q4']}\n"
        f"5. {message.text}\n\n"
        f"Пожалуйста, проанализируй и дай человечный психологический портрет состояния пользователя "
        f"и мягкие рекомендации по восстановлению. Обращайся по имени: {user_name}."
    )

    try:
        response = await ask_mia(user_id, user_name, prompt)
    except Exception as e:
        response = f"Мия временно недоступна. Ошибка: {e}"

    await message.answer(response)
