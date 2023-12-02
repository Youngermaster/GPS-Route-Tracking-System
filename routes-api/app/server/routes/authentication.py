from fastapi.security import OAuth2PasswordRequestForm
from server.utils import create_access_token
from passlib.context import CryptContext
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from server.database.user import add_user, retrieve_user_by_email
from server.models.user import UserSchema
from server.dependencies import get_current_user
from server.models.user import (
    ResponseModel,
    UserSchema,
)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Utility function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Utility function to hash password


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register", response_description="User data added into the database")
async def register_user(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    hashed_password = get_password_hash(user["password"])
    user["password"] = hashed_password
    new_user = await add_user(user)
    return ResponseModel(new_user, "User registered successfully.")


@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await retrieve_user_by_email(form_data.username)
    # Check if the 'password' key exists in the user dictionary
    if (
        not user
        or "password" not in user
        or not verify_password(form_data.password, user["password"])
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = {"sub": user["email"]}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}
