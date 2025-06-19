from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/finds', response_model=list[schemas.FindOut])
def list_finds(db: Session = Depends(get_db)):
    return crud.list_finds(db)
