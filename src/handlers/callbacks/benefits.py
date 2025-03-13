from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.keyboards.inline import InlineKeyboards
from src.model.db_functions import update_registration_step
from src.states.states import BenefitState

router = Router()


@router.callback_query(F.data == "check_benefits")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    """Запуск регистрации пользователя с начала."""
    await state.set_state(BenefitState.CHECK_BENEFITS)

    user_id = callback.from_user.id
    update_registration_step(user_id, "Нажали на получение льгот")

    await callback.message.answer(
        "Сервис будет разработан позднее:",
        reply_markup=InlineKeyboards.main_menu(user_id))