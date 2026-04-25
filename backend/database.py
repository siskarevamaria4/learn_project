import sqlite3

DB_NAME = "app.db"


def get_connection():
    """Получение соединения с БД"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Чтобы получать данные как словари
    return conn


def init_db():
    """Инициализация базы данных - создание таблицы books"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            publisher TEXT NOT NULL,
            pages INTEGER NOT NULL,
            isbn TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL DEFAULT 0,
            price REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("База данных инициализирована")