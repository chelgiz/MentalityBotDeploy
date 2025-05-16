import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN
from bot.handlers import (
    start, phq9, beck, spilberger, mfi20,
    burnout, special_interview, diagnostic_report,
    checkin, progress, sos, questions, relief
)

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем все роутеры
    dp.include_routers(
        start.router,
        phq9.router,
        beck.router,
        spilberger.router,
        mfi20.router,
        burnout.router,
        special_interview.router,
        diagnostic_report.router,
        checkin.router,
        progress.router,
        sos.router,
        questions.router,
        relief.router
    )

    print("✅ MentalityBot запущен.")
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
