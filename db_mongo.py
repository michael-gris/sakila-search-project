from pymongo import MongoClient
from pymongo.collection import Collection
import os
from dotenv import load_dotenv

# Загружаем .env из той же папки
load_dotenv()


def create_mongo_connection() -> Collection | None:
    """
    Возвращает коллекцию MongoDB из базы ich_edit.
    """
    mongodb_url = os.getenv("MONGODB_URL")
    mongodb_db = os.getenv("MONGODB_DBNAME")

    if not mongodb_url or not mongodb_db:
        print(
            "MongoDB ошибка подключения: MONGODB_URL или MONGODB_DBNAME не найдены в .env"
        )
        return None

    try:
        mongo_client = MongoClient(mongodb_url)
        mongo_db = mongo_client[mongodb_db]
        return mongo_db["final_project_100125dam_Michael_Gris"]
    except Exception as e:
        print(f"MongoDB ошибка подключения: {e}")
        return None
