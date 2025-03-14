from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.keyboards.inline import InlineKeyboards
from src.constants import message_constants
from src.model.db_functions import add_user  # Функция для добавления пользователя

router = Router()

@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    """Обработчик команды /start."""
    user_id = message.from_user.id
    add_user(user_id)

    await state.clear()

    await message.answer(
        message_constants.Messages.get_welcome_message(user_id) + "\nВыберите действие:",
        reply_markup=InlineKeyboards.main_menu(user_id)
    )
