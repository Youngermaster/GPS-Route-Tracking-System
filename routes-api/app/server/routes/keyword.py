from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.database.keyword import (
    add_keyword,
    add_keywords,
    delete_keyword,
    retrieve_keywords,
)

from server.models.keyword import KeywordSchema, KeywordsList
from server.models.keyword import (
    ErrorResponseModel,
    ResponseModel,
)

router = APIRouter()


@router.post("/bulk", response_description="Multiple keywords added to the database")
async def add_keywords_bulk(keywords: KeywordsList = Body(...)):
    added_keywords = await add_keywords(keywords.keywords)
    if added_keywords:
        return ResponseModel(added_keywords, "Keywords added successfully.")
    return ErrorResponseModel(
        "An error occurred", 400, "There was an error adding the keywords."
    )


@router.post("/", response_description="Keyword data added into the database")
async def add_keyword_data(keyword: KeywordSchema = Body(...)):
    keyword = jsonable_encoder(keyword)
    new_keyword = await add_keyword(keyword)
    return ResponseModel(new_keyword, "Keyword added successfully.")


@router.get("/", response_description="Keywords retrieved")
async def get_keywords():
    keywords = await retrieve_keywords()
    if keywords:
        return ResponseModel(keywords, "Keyword data retrieved successfully")
    return ResponseModel(keywords, "Empty list returned")


@router.delete("/{id}", response_description="Keyword data deleted from the database")
async def delete_keyword_data(id: str):
    deleted_keyword = await delete_keyword(id)
    if deleted_keyword:
        return ResponseModel(
            "Keyword with ID: {} removed".format(id), "Keyword deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Keyword with id {0} doesn't exist".format(id)
    )
