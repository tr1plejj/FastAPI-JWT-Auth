from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.exc import IntegrityError
from src.auth.dependencies import get_current_active_user
from src.auth.service import authenticate_user, create_jwt, hash_password
from src.auth.exceptions import incorrect_data, not_unique
from datetime import timedelta
from src.auth.config import TOKEN_EXPIRES_MINUTES
from src.auth.schemas import Token, User, UserInDB
from src.auth.database import async_session
from src.auth.models import User as UserOrm

router = APIRouter(tags=['auth'])


@router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise incorrect_data
    access_token_expires = timedelta(TOKEN_EXPIRES_MINUTES)
    access_token = await create_jwt({'sub': user.username}, access_token_expires)
    return Token(access_token=access_token, token_type='bearer')


@router.get('/users/me', response_model=User)
async def get_current_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.post('/register', response_model=User)
async def register(new_user: UserInDB):  # не принимать disabled
    try:
        async with async_session() as session:
            hashed_password = hash_password(new_user.hashed_password)
            user = UserOrm(username=new_user.username, hashed_password=hashed_password, email=new_user.email,
                           full_name=new_user.full_name, disabled=new_user.disabled)
            session.add(user)
            await session.commit()
        return User(**new_user.dict())
    except IntegrityError:
        raise not_unique
