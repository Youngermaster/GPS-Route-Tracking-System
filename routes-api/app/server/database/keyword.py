from bson.objectid import ObjectId
from .config import database

keyword_collection = database.get_collection("keywords_collection")


def keyword_helper(keyword) -> dict:
    return {
        "id": str(keyword["_id"]),
        "keyword": keyword["keyword"],
    }


async def retrieve_keywords():
    keywords = []
    async for keyword in keyword_collection.find():
        keywords.append(keyword_helper(keyword))
    return keywords


async def add_keyword(keyword_data: dict) -> dict:
    keyword = await keyword_collection.insert_one(keyword_data)
    new_keyword = await keyword_collection.find_one({"_id": keyword.inserted_id})
    return keyword_helper(new_keyword)


async def add_keywords(keywords_data: list) -> list:
    keywords = [{"keyword": keyword} for keyword in keywords_data]
    result = await keyword_collection.insert_many(keywords)
    if result.inserted_ids:
        return [str(id) for id in result.inserted_ids]
    return []


async def delete_keyword(id: str):
    keyword = await keyword_collection.find_one({"_id": ObjectId(id)})
    if keyword:
        await keyword_collection.delete_one({"_id": ObjectId(id)})
        return True
