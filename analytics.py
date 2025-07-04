from pymongo.collection import Collection
from datetime import datetime


def show_top_queries(mongo_collection: Collection | None) -> None:
    """
    Показывает топ-5 популярных типов поисковых запросов.

    Args:
        mongo_collection (Collection | None): MongoDB коллекция с логами.
    """
    if mongo_collection is None:
        print("MongoDB не подключена.")
        return

    pipeline = [
        {"$group": {"_id": "$search_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
    ]
    results = mongo_collection.aggregate(pipeline)

    print("Топ-5 популярных запросов:")
    for record in results:
        print(f"{record['_id']} — {record['count']} раз")

        from datetime import datetime  # ← если ещё не импортирован


def show_last_queries(mongo_collection: Collection | None, limit: int = 5) -> list:
    """
    Получает последние N (по умолчанию 5) запросов из MongoDB по дате (убывание).
    """
    if mongo_collection is None:
        print("MongoDB не подключена.")
        return []

    cursor = mongo_collection.find().sort("timestamp", -1).limit(limit)
    results = []

    for doc in cursor:
        timestamp = doc.get("timestamp")
        readable_time = (
            timestamp.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(timestamp, datetime)
            else str(timestamp)
        )
        query_type = doc.get("query_type", "—")
        details = doc.get("details", "—")
        results.append([readable_time, query_type, details])

    return results
