from db_mysql import create_mysql_connection
from db_mongo import create_mongo_connection
from search import search_by_keyword, search_by_genre_and_year
from analytics import show_top_queries, show_last_queries
import ui


def main() -> None:
    """
    Главная точка входа. Меню и логика управления.
    """
    mysql_connection = create_mysql_connection()
    mongo_collection = create_mongo_connection()

    if not mysql_connection:
        print("Нет подключения к MySQL. Завершаем работу.")
        return

    while True:
        ui.print_menu()
        choice = ui.get_user_input("Введите номер действия: ")

        if choice == "1":
            search_by_keyword(mysql_connection, mongo_collection)
        elif choice == "2":
            search_by_genre_and_year(mysql_connection, mongo_collection)
        elif choice == "3":
            show_top_queries(mongo_collection)
        elif choice == "4":
            results = show_last_queries(mongo_collection)
            ui.display_results(results, headers=["Дата", "Тип запроса", "Детали"])
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
