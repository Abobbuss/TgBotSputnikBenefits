from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import load_config

from src.keyboards.inline import InlineKeyboards
from src.model.db_functions import get_user_statistics

router = Router()
config = load_config()

print("Admin router loaded")  # Проверка загрузки админ-роутера

@router.callback_query(F.data == "statistics")  # Теперь правильно ловим callback-кнопку
async def send_statistics(callback: CallbackQuery):
    """Обрабатывает нажатие кнопки 'Получить статистику'."""
    user_id = callback.from_user.id
    if user_id not in config.tg_bot.admins:
        await callback.answer("У вас нет прав для просмотра статистики.", show_alert=True)
        return

    total_users, step_counts = get_user_statistics()

    stats_text = f"📊 <b>Статистика пользователей</b>\n\n"
    stats_text += f"👥 Всего пользователей: {total_users}\n\n"
    stats_text += "📌 Количество пользователей на каждом шаге регистрации:\n"
    for step, count in step_counts.items():
        stats_text += f"  🔹 {step.replace('_', ' ').title()}: {count}\n"

    await callback.message.answer(stats_text, parse_mode="HTML", reply_markup=InlineKeyboards.main_menu(user_id))
