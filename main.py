import os
from dotenv import load_dotenv
from mysql.connector import connect, Error
from pymongo import MongoClient
from datetime import datetime

# Загружаем переменные окружения из .env файла
load_dotenv()

# Подключение к MySQL
def create_mysql_connection():
    try:
        connection = connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
        return connection
    except Error as e:
        print(f"MySQL ошибка подключения: {e}")
        return None

# Подключение к MongoDB (логирование)
def create_mongo_connection():
    try:
        mongo_client = MongoClient("mongodb://localhost:27017/")
        mongo_db = mongo_client["sakila_logs"]
        return mongo_db["queries"]
    except Exception as e:
        print(f"MongoDB ошибка подключения: {e}")
        return None

# Поиск по ключевому слову
def search_by_keyword(connection, mongo_collection):
    keyword = input("Введите часть названия фильма: ")
    cursor = connection.cursor()
    query = """
        SELECT film_id, title, release_year, rating
        FROM film
        WHERE title LIKE %s
    """
    cursor.execute(query, (f"%{keyword}%",))
    results = cursor.fetchall()

    # Вывод результатов
    count = 0
    for row in results:
        print(f"{row[0]} — {row[1]} ({row[2]}), Rating: {row[3]}")
        count += 1
        if count % 10 == 0:
            more = input("Показать ещё 10? (y/n): ")
            if more.lower() != 'y':
                break

    # Сохраняем лог
    if mongo_collection:
        mongo_collection.insert_one({
            "timestamp": datetime.now(),
            "search_type": "keyword",
            "params": {"keyword": keyword},
            "results_count": len(results)
        })

# Поиск по жанру и году
def search_by_genre_and_year(connection, mongo_collection):
    try:
        category_id = int(input("Введите ID жанра (например, 5): "))
        year_from = int(input("Год от: "))
        year_to = int(input("Год до: "))
    except ValueError:
        print("Ошибка ввода. Введите числа.")
        return

    cursor = connection.cursor()
    query = """
        SELECT f.film_id, f.title, f.release_year, c.name
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s
    """
    cursor.execute(query, (category_id, year_from, year_to))
    results = cursor.fetchall()

    count = 0
    for row in results:
        print(f"{row[0]} — {row[1]} ({row[2]}), Жанр: {row[3]}")
        count += 1
        if count % 10 == 0:
            more = input("Показать ещё 10? (y/n): ")
            if more.lower() != 'y':
                break

    if mongo_collection:
        mongo_collection.insert_one({
            "timestamp": datetime.now(),
            "search_type": "genre_year",
            "params": {"category_id": category_id, "year_from": year_from, "year_to": year_to},
            "results_count": len(results)
        })

# Топ-5 популярных запросов
def show_top_queries(mongo_collection):
    if not mongo_collection:
        print("MongoDB не подключена.")
        return

    pipeline = [
        {"$group": {"_id": "$search_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    results = mongo_collection.aggregate(pipeline)

    print("Топ-5 популярных запросов:")
    for r in results:
        print(f"{r['_id']} — {r['count']} раз")

# Главное меню
def main():
    mysql_connection = create_mysql_connection()
    mongo_collection = create_mongo_connection()

    if not mysql_connection:
        print("Нет подключения к MySQL. Завершаем работу.")
        return

    while True:
        print("\nМеню:")
        print("1. Поиск по ключевому слову (названию)")
        print("2. Поиск по жанру и году")
        print("3. Топ-5 популярных запросов")
        print("0. Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            search_by_keyword(mysql_connection, mongo_collection)
        elif choice == "2":
            search_by_genre_and_year(mysql_connection, mongo_collection)
        elif choice == "3":
            show_top_queries(mongo_collection)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
