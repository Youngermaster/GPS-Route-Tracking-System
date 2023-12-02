from typing import List, Tuple
from pydantic import BaseModel, Field
from bson import ObjectId

class RouteSchema(BaseModel):
    route_id: str = Field(...)
    name: str = Field(...)
    isProcessed: bool = Field(...)
    isFinished: bool = Field(...)
    directions: List[Tuple[float, float]] = Field(...)
    polyline: List[Tuple[float, float]] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "route_id": "route-123",
                "name": "Route A-B-C-A",
                "isProcessed": False,
                "isFinished": False,
                "directions": [],
                "polyline": []
            }
        }

class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return str(v)
