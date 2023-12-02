from typing import List
from pydantic import BaseModel, Field


class KeywordSchema(BaseModel):
    keyword: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "keyword": "astronomy",
            }
        }


class KeywordsList(BaseModel):
    keywords: List[str]

    class Config:
        schema_extra = {
            "example": {
                "keywords": ["ABC", "DEF", "GHI"],
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
