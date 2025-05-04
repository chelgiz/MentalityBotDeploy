from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.main_keyboard import main_menu
from bot.services.openai_assistant import ask_mia

router = Router()

questions = [
    "Как ты обычно реагируешь на неожиданные изменения в жизни?",
    "Что для тебя является источником внутренней силы?",
    "Чего ты боишься больше всего?",
    "Как ты восстанавливаешься после тяжёлого дня?",
    "Что тебя вдохновляет?",
    "Ты скорее интроверт или экстраверт?",
    "Насколько легко тебе доверять другим людям?",
    "Как ты справляешься с чувством одиночества?",
    "Что для тебя значит счастье?",
    "Есть ли у тебя цели, о которых ты пока никому не говорил?",
    "Как ты ведёшь себя в конфликтных ситуациях?",
    "Что бы ты изменил в себе, если бы мог?",
    "Какие три слова лучше всего описывают твою личность?",
    "Как ты понимаешь, что тебе сейчас нужна поддержка?",
    "Что тебе помогает принять трудное решение?",
    "Когда ты в последний раз чувствовал(а) себя по-настоящему живым?",
    "Какую роль играет страх в твоей жизни?",
    "Какие качества ты больше всего ценишь в людях?",
    "Что для тебя значит быть «собой»?",
    "Если бы ты мог поговорить с собой в детстве — что бы ты сказал(а)?"
]


class Interview(StatesGroup):
    Q = State()
    Result = State()


@router.message(F.text == "🧠 Спецопрос")
async def start_interview(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(answers=[])
    await state.update_data(q_index=0)
    await message.answer("🧬 Я задам тебе 20 вопросов, чтобы лучше понять тебя. Готов(а)?")
    await message.answer(questions[0])
    await state.set_state(Interview.Q)


@router.message(Interview.Q)
async def handle_question(message: Message, state: FSMContext):
    data = await state.get_data()
    answers = data.get("answers", [])
    q_index = data.get("q_index", 0)

    answers.append(message.text)
    q_index += 1

    if q_index < len(questions):
        await state.update_data(answers=answers, q_index=q_index)
        await message.answer(questions[q_index])
    else:
        await message.answer("💡 Благодарю тебя за искренность. Сейчас я подведу итоги...")
        await state.set_state(Interview.Result)

        user_profile = "\n".join(
            [f"{i + 1}. {q}\nОтвет: {a}" for i, (q, a) in enumerate(zip(questions, answers))]
        )

        summary_prompt = f"""
Вот ответы пользователя на психологический спецопрос. На основе этого составь мягкий, эмпатичный психологический портрет. 
Укажи особенности характера, сильные стороны, возможные уязвимости. Не давай диагнозов. Пиши от лица Мии, как заботливый ассистент.

{user_profile}
"""
        result = ask_mia(summary_prompt)
        await message.answer(result)
        await message.answer("🌿 Возвращаю тебя в главное меню.", reply_markup=main_menu())
        await state.clear()
