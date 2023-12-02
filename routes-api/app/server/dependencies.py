from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from server.utils import decode_access_token
from server.database.user import retrieve_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await retrieve_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
