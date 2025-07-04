from datetime import datetime
from mysql.connector import MySQLConnection
from pymongo.collection import Collection


def search_by_keyword(
    connection: MySQLConnection, mongo_collection: Collection | None
) -> None:
    """
    Поиск фильмов по части названия.

    Args:
        connection (MySQLConnection): Подключение к MySQL.
        mongo_collection (Collection | None): MongoDB коллекция для логирования.
    """
    keyword = input("Введите часть названия фильма: ")
    cursor = connection.cursor()
    query = """
        SELECT film_id, title, release_year, rating
        FROM film
        WHERE title LIKE %s
    """
    cursor.execute(query, (f"%{keyword}%",))
    results = cursor.fetchall()

    count = 0
    for row in results:
        print(f"{row[0]} — {row[1]} ({row[2]}), Rating: {row[3]}")
        count += 1
        if count % 10 == 0:
            more = input("Показать ещё 10? (y/n): ")
            if more.lower() != "y":
                break

    if mongo_collection is not None:
        mongo_collection.insert_one(
            {
                "timestamp": datetime.now(),
                "query_type": "keyword",
                "details": keyword,
                "results_count": len(results),
            }
        )


def search_by_genre_and_year(
    connection: MySQLConnection, mongo_collection: Collection | None
) -> None:
    """
    Поиск фильмов по жанру и диапазону годов.

    Args:
        connection (MySQLConnection): Подключение к MySQL.
        mongo_collection (Collection | None): MongoDB коллекция для логирования.
    """
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
            if more.lower() != "y":
                break

    if mongo_collection is not None:
        mongo_collection.insert_one(
            {
                "timestamp": datetime.now(),
                "query_type": "genre_year",
                "details": f"genre_id={category_id}, years={year_from}-{year_to}",
                "results_count": len(results),
            }
        )
