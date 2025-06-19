from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/affiliate/{user_id}', response_model=schemas.AffiliateOut)
def read_affiliate(user_id: int, db: Session = Depends(get_db)):
    stat = db.query(models.Affiliate).filter(models.Affiliate.user_id == user_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail='Stats not found')
    return stat


@router.post('/affiliate/{user_id}/withdraw', response_model=schemas.AffiliateOut)
def request_withdraw(user_id: int, db: Session = Depends(get_db)):
    stat = db.query(models.Affiliate).filter(models.Affiliate.user_id == user_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail='Stats not found')
    stat.withdraw_requested = True
    db.commit()
    db.refresh(stat)
    return stat
