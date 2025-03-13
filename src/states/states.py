from aiogram.fsm.state import State, StatesGroup

class RegistrationState(StatesGroup):
    START = State()               # Начало регистрации (нажатие "Внести информацию о себе")
    GENDER = State()              # Выбор пола
    MARITAL_STATUS = State()      # Выбор семейного положения
    CHILDREN_COUNT = State()      # Ввод количества детей
    CHILDREN_AGES = State()       # Ввод возраста детей
    COMPLETED = State()           # Регистрация завершена

class BenefitState(StatesGroup):
    CHECK_BENEFITS = State()      # Состояние, когда пользователь нажал "Узнать льготы"
