from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from fastapi.responses import UJSONResponse

from ..dependency import get_mysql
from ..db.crud import get_users
from ..schemas import UserDetail

router = APIRouter()

@router.get(path='', response_model=List[UserDetail])
async def read_many_users(
    _end: int = Query(100, title="query index end"),
    _order: str = Query('ASC', title="ASC DES"),
    _sort: str = Query('id', title="default sort field"),
    _start: int = Query(1, title="query index start"),
    db: Session = Depends(get_mysql),
):
    users = await get_users(db, _start, _end, _sort, _order)
    return users