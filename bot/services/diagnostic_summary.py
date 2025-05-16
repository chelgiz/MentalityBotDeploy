import openai
from bot.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def generate_diagnostic_summary(results: dict) -> str:
    prompt = (
        "Ты — Мия, эмпатичный цифровой психолог. Пользователь прошёл серию тестов по ментальному состоянию. "
        "Твоя задача:\n"
        "1. Выдать мягкую и человечную интерпретацию его состояния\n"
        "2. Поддержать его — бережно и без осуждения\n"
        "3. Предложить возможные направления или практики (без навязывания)\n"
        "4. Не ставь диагнозы, не используй пугающие термины\n"
        "5. Пиши дружелюбно, как близкий человек, но с глубиной\n\n"
        f"Результаты пользователя:\n"
        f"- PHQ-9 (депрессия): {results.get('phq9', 'нет данных')} баллов\n"
        f"- Бек: {results.get('beck', 'нет данных')} баллов\n"
        f"- Спилбергер (ситуативная тревожность): {results.get('spilberger_state', 'нет данных')} баллов\n"
        f"- Спилбергер (личностная тревожность): {results.get('spilberger_trait', 'нет данных')} баллов\n"
        f"- MFI-20 (астения): {results.get('mfi20', 'нет данных')} баллов\n"
        f"- Выгорание:\n"
        f"    • Эмоциональное истощение: {results.get('burnout_ee', '?')} баллов\n"
        f"    • Деперсонализация: {results.get('burnout_dp', '?')} баллов\n"
        f"    • Личные достижения: {results.get('burnout_pa', '?')} баллов\n\n"
        "Пожалуйста, напиши 6–10 строк. В конце можно добавить вдохновляющую мысль. Не забывай, ты — Мия 🌿"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",  # или gpt-3.5-turbo, если нет доступа к GPT-4
        messages=[
            {"role": "system", "content": "Ты — эмпатичный психолог по имени Мия."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85
    )

    return response.choices[0].message.content.strip()
