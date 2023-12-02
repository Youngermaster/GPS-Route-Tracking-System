from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class UserSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: str = Field(...)
    phone: str = Field(...)
    avatar: HttpUrl = Field(...)
    hiredDate: str = Field(...)
    skills: List[str] = Field(default=[])

    class Config:
        schema_extra = {
            "example": {
                "name": "Mahedi Amin",
                "email": "mahedi@example.com",
                "password": "hashed_password_here",
                "role": "Technician",
                "phone": "123-456-7890",
                "avatar": "https://example.com/path_to_avatar_image.jpg",
                "hiredDate": "2022-10-03",
                "skills": ["Engine Repair", "Oil Change"],
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[str]
    phone: Optional[str]
    avatar: Optional[HttpUrl]
    hiredDate: Optional[str]
    skills: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "name": "Mahedi Amin",
                "email": "mahedi@example.com",
                "password": "new_hashed_password_here",
                "role": "Technician",
                "phone": "123-456-7890",
                "avatar": "https://example.com/path_to_avatar_image.jpg",
                "hiredDate": "2022-10-03",
                "skills": ["Engine Repair", "Oil Change"],
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
