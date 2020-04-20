from functools import lru_cache
from datetime import datetime
import os

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from .config import setting
from .db.connect import Base, Engine, Session
from .db.crud import get_authenticate_user, get_user, create_user
from .routers import UserRouter, TaskRouter
from .schemas import UserDetail, TokenData, User, UserIn
from .utils import decode_token, create_access_token
from .dependency import get_mysql

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]


@lru_cache()
def get_settings():
    return setting

Base.metadata.create_all(bind=Engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_mysql)):
    user = await get_authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise credentials_exception
    access_token = create_access_token(data={"sub":user.username, "role":"test_admin"})
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_mysql)) -> UserDetail:
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception

    # mmmmmmmm
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post('/register', response_model=User, status_code=status.HTTP_201_CREATED)
async def register(request: Request, user: UserIn, db: Session = Depends(get_mysql)):
    existing_user = await get_user(db, username=user.username)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='user already exist',
        )

    new_user = await create_user(db, user.username, user.password)
    return new_user

app.include_router(
    UserRouter,
    prefix="/user",
    tags=["users"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"msg": "Content Not found"}},
)

app.include_router(
    TaskRouter,
    prefix="/task",
    tags=["tasks"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"msg": "Content Not found"}},
)
