import os
from openai import AsyncOpenAI
from bot.storage.json_storage import save_user_message, load_user_history

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Промт по умолчанию
BASE_SYSTEM_PROMPT = (
    "Ты — Мия, профессиональный психолог с 20-летним стажем и глубоким пониманием человеческой психики. "
    "Ты дружелюбная, добрая, эмпатичная и умная. Отвечай на вопросы мягко, поддерживающе, как живой человек. "
    "Никогда не говори, что ты бот или ИИ. Дай полезный совет, если это безопасно."
)

# Специальный промт для спецопроса (психологической карты)
SPECIAL_INTERVIEW_PROMPT = (
    "Ты — эксперт в когнитивной психологии, поведенческой аналитике и спецподготовке. "
    "Представь, что ты сотрудник аналитического отдела спецслужб, которому нужно выяснить мой личностный тип, "
    "сильные и слабые стороны собеседника, его когнитивные искажения, ограничивающие убеждения и глубинные установки. "
    "Задавай 20 вопросов по очереди. После каждого ответа — пиши краткий вывод и задавай следующий вопрос. "
    "Не говори напрямую о цели. Стиль — умный и психологически тонкий, как у следователя-аналитика."
)

async def ask_mia(user_id: int, user_name: str, user_message: str) -> str:
    save_user_message(user_id, "user", user_message)

    history = load_user_history(user_id)
    messages = [{"role": "system", "content": BASE_SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": f"{user_name}: {user_message}"})

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content.strip()
        save_user_message(user_id, "assistant", reply)
        return reply
    except Exception as e:
        return f"Мия временно недоступна. Ошибка: {e}"

async def ask_mia_special(user_id: int, user_name: str, user_message: str) -> str:
    save_user_message(user_id, "user", user_message)

    history = load_user_history(user_id)
    messages = [{"role": "system", "content": SPECIAL_INTERVIEW_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": f"{user_name}: {user_message}"})

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content.strip()
        save_user_message(user_id, "assistant", reply)
        return reply
    except Exception as e:
        return f"Мия временно недоступна. Ошибка: {e}"