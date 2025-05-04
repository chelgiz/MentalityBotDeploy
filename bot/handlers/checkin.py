from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.services.openai_assistant import ask_mia
from bot.keyboards.main_keyboard import main_menu

router = Router()

class CheckInStates(StatesGroup):
    mood = State()
    energy = State()
    motivation = State()

@router.message(lambda msg: msg.text == "✅ Чек-ин")
async def start_checkin(message: types.Message, state: FSMContext):
    await message.answer("Чек-ин 🌅\n\nКак ты оцениваешь своё **настроение** от 1 до 10?")
    await state.set_state(CheckInStates.mood)

@router.message(CheckInStates.mood)
async def checkin_mood(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10.")
        return
    await state.update_data(mood=int(message.text))
    await message.answer("Как ты оцениваешь свою **энергию** от 1 до 10?")
    await state.set_state(CheckInStates.energy)

@router.message(CheckInStates.energy)
async def checkin_energy(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10.")
        return
    await state.update_data(energy=int(message.text))
    await message.answer("Как ты оцениваешь свою **мотивацию** от 1 до 10?")
    await state.set_state(CheckInStates.motivation)

@router.message(CheckInStates.motivation)
async def checkin_motivation(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10.")
        return
    await state.update_data(motivation=int(message.text))
    data = await state.get_data()
    await state.clear()

    # Подготовка текста для анализа Мией
    prompt = (
        f"Пользователь прошёл утренний чек-ин. Настроение: {data['mood']}/10, энергия: {data['energy']}/10, мотивация: {data['motivation']}/10.\n"
        f"Сделай мягкий и поддерживающий анализ состояния. Если оценки низкие, предложи простые и добрые рекомендации."
    )
    response = await ask_mia(prompt)

    await message.answer(f"Спасибо за честность 🌿\n\n{response}", reply_markup=main_menu())
