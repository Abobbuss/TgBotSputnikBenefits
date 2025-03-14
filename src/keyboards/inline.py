from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import load_config
from src.model.db_functions import get_user_progress

config = load_config()

class InlineKeyboards:
    @staticmethod
    def main_menu(user_id: int):
        """Генерация главного меню в зависимости от статуса пользователя."""
        is_registered, _ = get_user_progress(user_id) or (0, None)  # Получаем статус регистрации

        buttons = []
        if is_registered:
            buttons.append([InlineKeyboardButton(text="Оплатить и получить список льгот", callback_data="check_benefits")])
        else:
            buttons.append([InlineKeyboardButton(text="Начать", callback_data="start_registration")])

        # Добавляем кнопку статистики для админов
        if user_id in config.tg_bot.admins:
            buttons.append([InlineKeyboardButton(text="Получить статистику", callback_data="statistics")])

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def gender_buttons():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Мужчина", callback_data="gender_male")],
                [InlineKeyboardButton(text="Женщина", callback_data="gender_female")]
            ]
        )

    @staticmethod
    def marital_status_buttons():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="В браке", callback_data="marital_married")],
                [InlineKeyboardButton(text="Не в браке", callback_data="marital_single")]
            ]
        )

    @staticmethod
    def children_count_buttons():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=str(i), callback_data=f"children_{i}")]
                for i in range(10)
            ]
        )
