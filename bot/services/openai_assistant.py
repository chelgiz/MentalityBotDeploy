import os
from openai import OpenAI

client = OpenAI()

async def ask_mia(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — эмпатичный психолог по имени Мия. Отвечай мягко, поддерживающе, на человеческом языке. Всегда давай понятные рекомендации, если запрос касается ментального состояния."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI error: {e}"
