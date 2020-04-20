from sqlalchemy.orm import Session

from . import models
from ..utils import hash_password, verify_password


async def get_user(db: Session, user_id: int=None, username: str=None, email:str=None):
    if user_id:
        return db.query(models.User).filter_by(id=user_id).first()
    if username:
        return db.query(models.User).filter_by(username=username).first()
    if email:
        return db.query(models.User).filter_by(email=email).first()

async def get_authenticate_user(db: Session, username: str, password:str):
    user = await get_user(db, username=username)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user

async def get_users(db: Session, _start, _end, _sort, _order):
    return db.query(models.User).offset(_start).limit(_end).all()

async def create_user(db: Session, username, password):
    user = models.User(username=username, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def create_by_file(db: Session, table:str, data:dict):
    if table == "user":
        user = models.User(username=data['username'], password_hash=hash_password(data['password']))
        db.add(user)
    elif table == "task":
        task = models.Tasks(**data)
        db.add(task)
    elif table == "client":
        client = models.Client(**data)
        db.add(client)
