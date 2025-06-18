from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/users/{user_id}', response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    result = schemas.UserOut.from_orm(user)
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


@app.patch('/users/{user_id}', response_model=schemas.UserOut)
def update_user(user_id: int, data: schemas.UserBase, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if data.location is not None:
        user.location = data.location
    db.commit()
    db.refresh(user)
    return read_user(user_id, db)
