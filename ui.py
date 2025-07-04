from tabulate import tabulate


def print_menu():
    print("\nВыберите действие:")
    print("1. Поиск фильма по названию")
    print("2. Поиск по жанру и диапазону лет")
    print("3. Топ-5 популярных запросов")
    print("4. Последние 5 запросов")
    print("5. Выход")


def get_user_input(prompt):
    return input(prompt)


def display_results(results, headers):
    if not results:
        print("Нет данных для отображения.")
    else:
        print(tabulate(results, headers=headers, tablefmt="grid"))
