from pymongo.collection import Collection


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
