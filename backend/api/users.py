from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/users/{user_id}', response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
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
def update_user(user_id: int, data: schemas.UserBase, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if data.location is not None:
        user.location = data.location
    db.commit()
    db.refresh(user)
    return read_user(user_id, db)
