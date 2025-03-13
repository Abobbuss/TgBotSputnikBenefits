import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "database.db")

def init_db():
    """Инициализирует базу данных, если она не существует."""
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as db:
            cursor = db.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    is_registered BOOLEAN NOT NULL DEFAULT 0,  -- Зарегистрирован ли пользователь
                    registration_step TEXT DEFAULT NULL,       -- На каком шаге остановился
                    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            db.commit()

def add_user(telegram_id):
    """Добавляет пользователя в базу данных, если его там еще нет."""
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("INSERT OR IGNORE INTO Users (telegram_id) VALUES (?)", (telegram_id,))
        db.commit()

def update_registration_step(telegram_id, step):
    """Обновляет текущий шаг регистрации пользователя."""
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("UPDATE Users SET registration_step = ? WHERE telegram_id = ?", (step, telegram_id))
        db.commit()

def mark_as_registered(telegram_id):
    """Помечает пользователя как зарегистрированного."""
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("UPDATE Users SET is_registered = 1 WHERE telegram_id = ?", (telegram_id,))
        db.commit()

def get_user_progress(telegram_id):
    """Возвращает статус регистрации и текущий шаг пользователя."""
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT is_registered, registration_step FROM Users WHERE telegram_id = ?", (telegram_id,))
        return cursor.fetchone()  # (is_registered, registration_step) или None

def get_user_statistics():
    """Получает статистику по пользователям."""
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()

        # 1. Общее количество пользователей
        cursor.execute("SELECT COUNT(*) FROM Users")
        total_users = cursor.fetchone()[0]

        # 2. Количество пользователей на каждом шаге регистрации
        cursor.execute("""
            SELECT registration_step, COUNT(*) 
            FROM Users 
            WHERE registration_step IS NOT NULL 
            GROUP BY registration_step
        """)
        step_counts = dict(cursor.fetchall())

    return total_users, step_counts
