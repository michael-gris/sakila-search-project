import os
from mysql.connector import connect, Error
from dotenv import load_dotenv

# Загружаем .env из папки уровнем выше
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def create_mysql_connection():
    """
    Создаёт и возвращает подключение к MySQL базе данных.

    Returns:
        connection (mysql.connector.connection.MySQLConnection | None):
            Подключение к базе или None при ошибке.
    """
    try:
        connection = connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
        )
        return connection
    except Error as e:
        print(f"MySQL ошибка подключения: {e}")
        return None
