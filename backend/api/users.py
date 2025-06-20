from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/users/{user_id}', response_model=schemas.UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    result = schemas.UserOut.model_validate(user)
    if user.join_date:
        result.days_in_club = (date.today() - user.join_date).days
    if result.days_in_club is not None:
        d = result.days_in_club
        if d < 30:
            result.status = 'Новичок'
        elif d < 180:
            result.status = 'Агент'
        elif d < 365:
            result.status = 'Партнёр'
        else:
            result.status = 'Ветеран'
    return result


@router.patch('/users/{user_id}', response_model=schemas.UserOut)
async def update_user(user_id: int, data: schemas.UserBase, db: AsyncSession = Depends(get_db)):
    user = await crud.update_user(db, user_id, location=data.location)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return await read_user(user_id, db)


@router.post('/users/{user_id}/pay', response_model=schemas.UserOut)
async def pay_membership(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.set_membership(db, user_id, True)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return await read_user(user_id, db)

