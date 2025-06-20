from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/affiliate/{user_id}', response_model=schemas.AffiliateOut)
async def read_affiliate(user_id: int, db: AsyncSession = Depends(get_db)):
    stat = await crud.get_affiliate(db, user_id)
    if not stat:
        raise HTTPException(status_code=404, detail='Stats not found')
    return stat


@router.post('/affiliate/{user_id}/withdraw', response_model=schemas.AffiliateOut)
async def request_withdraw(user_id: int, db: AsyncSession = Depends(get_db)):
    stat = await crud.request_withdraw(db, user_id)
    if not stat:
        raise HTTPException(status_code=404, detail='Stats not found')
    return stat

