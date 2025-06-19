from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/finds', response_model=list[schemas.FindOut])
def list_finds(db: Session = Depends(get_db)):
    items = db.query(models.Find).order_by(models.Find.created_at.desc()).all()
    return items
