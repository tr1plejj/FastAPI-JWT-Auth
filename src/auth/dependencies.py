import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
from jwt import InvalidTokenError
from src.auth.config import ALGORITHM, SECRET_KEY
from src.auth.exceptions import disabled_user, credentials_error
from src.auth.schemas import TokenData, User
from src.auth.service import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_error
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_error
    user = await get_user(token_data.username)
    if user is None:
        raise credentials_error
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise disabled_user
    return current_user
