from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards.main_keyboard import main_menu
from bot.services.openai_assistant import ask_mia

router = Router()

class PHQ9(StatesGroup):
    q0 = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()

questions = [
    "Вопрос 1 PHQ-9: Мало интереса или удовольствия от деятельности?",
    "Вопрос 2: Чувство подавленности, депрессии или безнадежности?",
    "Вопрос 3: Проблемы со сном (трудности засыпания, частые пробуждения, чрезмерный сон)?",
    "Вопрос 4: Усталость или недостаток энергии?",
    "Вопрос 5: Потеря аппетита или переедание?",
    "Вопрос 6: Низкая самооценка, ощущение собственной никчемности или вины?",
    "Вопрос 7: Трудности с концентрацией внимания (например, при чтении газеты или просмотре ТВ)?",
    "Вопрос 8: Медлительность или, наоборот, излишняя суетливость, замеченная другими?",
    "Вопрос 9: Мысли о самоповреждении или что вы лучше бы умерли?"
]

options = ["0 — совсем нет", "1 — несколько дней", "2 — более половины дней", "3 — почти каждый день"]

states = [
    PHQ9.q0, PHQ9.q1, PHQ9.q2, PHQ9.q3,
    PHQ9.q4, PHQ9.q5, PHQ9.q6, PHQ9.q7, PHQ9.q8
]

@router.message(F.text == "🧾 PHQ-9")
async def start_phq9(message: Message, state: FSMContext):
    await state.set_state(PHQ9.q0)
    await state.set_data({"answers": []})
    await message.answer("📋 Сейчас ты пройдёшь тест PHQ-9. Отвечай по шкале от 0 до 3.")
    await message.answer(questions[0], reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in options],
        resize_keyboard=True,
        one_time_keyboard=True
    ))

@router.message(PHQ9.q0)
@router.message(PHQ9.q1)
@router.message(PHQ9.q2)
@router.message(PHQ9.q3)
@router.message(PHQ9.q4)
@router.message(PHQ9.q5)
@router.message(PHQ9.q6)
@router.message(PHQ9.q7)
@router.message(PHQ9.q8)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    answers = data.get("answers", [])

    try:
        score = int(message.text.split("—")[0].strip())
        answers.append(score)
    except:
        await message.answer("Пожалуйста, выбери вариант из предложенных.")
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
        await message.answer("✅ Тест завершён. Подготавливаю результат...", reply_markup=main_menu())

        prompt = f"""Я только что прошёл тест PHQ-9, шкала депрессии. Мой итоговый балл: {total} из 27.
Расскажи мне, пожалуйста, что это может значить, как это интерпретируется с психологической точки зрения, и что бы ты порекомендовала в зависимости от результата? Объясни по-человечески."""

        response = await ask_mia(prompt)
        await message.answer(response)
