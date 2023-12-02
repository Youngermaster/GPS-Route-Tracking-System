from decouple import config


class Settings:
    SECRET_KEY: str = config("SECRET_KEY", default="YOUR_DEFAULT_SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int
    )
