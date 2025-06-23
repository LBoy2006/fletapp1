from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/finds/categories1')
async def get_categories1(db: AsyncSession = Depends(get_db)):
    return await crud.list_find_categories1(db)


@router.get('/finds/categories2')
async def get_categories2(categories1: str = '', db: AsyncSession = Depends(get_db)):
    cats1 = [c.strip() for c in categories1.split(',') if c.strip()]
    return await crud.list_find_categories2(db, cats1)


@router.get('/finds', response_model=list[schemas.FindOut])
async def list_finds(
    categories1: str = '',
    categories2: str = '',
    db: AsyncSession = Depends(get_db)
):
    cats1 = [c.strip() for c in categories1.split(',') if c.strip()]
    cats2 = [c.strip() for c in categories2.split(',') if c.strip()]
    return await crud.list_finds(db, cats1, cats2)

