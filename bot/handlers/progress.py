from aiogram import Router, F
from aiogram.types import Message
from bot.services.progress_chart import generate_checkin_plot
from bot.keyboards.main_keyboard import main_menu

router = Router()

@router.message(F.text.lower().contains("прогресс"))
async def show_progress(message: Message):
    image_path = generate_checkin_plot(user_id=message.from_user.id)
    if image_path:
        with open(image_path, "rb") as photo:
            await message.answer_photo(photo, caption="📈 Вот твоя динамика состояний.")
    else:
        await message.answer("У тебя пока нет данных для графика.")
    await message.answer("⬅️ Возвращаемся в главное меню.", reply_markup=main_menu())
