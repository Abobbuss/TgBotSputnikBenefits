from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.keyboards.inline import InlineKeyboards
from src.model.db_functions import update_registration_step, mark_as_registered
from src.states.states import RegistrationState

router = Router()


@router.callback_query(F.data == "start_registration")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    """Запуск регистрации пользователя с начала."""
    await state.set_state(RegistrationState.GENDER)

    user_id = callback.from_user.id
    update_registration_step(user_id, "Пол")

    await callback.message.answer(
        "Выберите ваш пол:",
        reply_markup=InlineKeyboards.gender_buttons()
    )

@router.callback_query(F.data.startswith("gender_"))
async def process_gender_selection(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор пола и переходит к выбору семейного положения."""
    user_id = callback.from_user.id
    gender = callback.data.split("_")[1]

    update_registration_step(user_id, "Семейное положение")

    await state.set_state(RegistrationState.MARITAL_STATUS)

    await callback.message.answer(
        "Выберите ваше семейное положение:",
        reply_markup=InlineKeyboards.marital_status_buttons()
    )

@router.callback_query(F.data.startswith("marital_"))
async def process_marital_status_selection(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор семейного положения и переходит к вопросу о количестве детей."""
    user_id = callback.from_user.id
    marital_status = callback.data.split("_")[1]  # Получаем "married" или "single"

    # Обновляем шаг регистрации в БД
    update_registration_step(user_id, "Количество детей")

    await state.set_state(RegistrationState.CHILDREN_COUNT)

    await callback.message.answer(
        "Укажите количество детей:",
        reply_markup=InlineKeyboards.children_count_buttons()
    )

@router.callback_query(F.data.startswith("children_"))
async def process_children_count(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор количества детей и переходит к следующему шагу."""
    user_id = callback.from_user.id
    children_count = int(callback.data.split("_")[1])  # Получаем количество детей

    if children_count > 0:
        # Если есть дети, запрашиваем их возраст
        update_registration_step(user_id, "Возраст детей")
        await state.set_state(RegistrationState.CHILDREN_AGES)
        await callback.message.answer("Введите возраст ваших детей через запятую (например: 3, 7, 10):")
    else:
        # Если детей нет – завершаем регистрацию
        update_registration_step(user_id, "Закончили регистрацию")
        mark_as_registered(user_id)

        await state.clear()
        await callback.message.answer(
            "Регистрация завершена! Теперь вы можете узнать, какие льготы вам доступны.",
            reply_markup=InlineKeyboards.main_menu(user_id)
        )


@router.message(RegistrationState.CHILDREN_AGES)
async def process_children_ages(message: Message, state: FSMContext):
    """Обрабатывает ввод возрастов детей и завершает регистрацию."""
    user_id = message.from_user.id
    children_ages = message.text.strip()

    # Проверяем корректность ввода (только цифры и запятые)
    if not all(age.strip().isdigit() for age in children_ages.split(",")):
        await message.answer("Ошибка! Введите возраст детей через запятую (например: 3, 7, 10).")
        return

    # Завершаем регистрацию
    update_registration_step(user_id, "Закончили регистрацию")
    mark_as_registered(user_id)

    await state.clear()
    await message.answer(
        "Регистрация завершена! Теперь вы можете узнать, какие льготы вам доступны.",
        reply_markup=InlineKeyboards.main_menu(user_id)
    )