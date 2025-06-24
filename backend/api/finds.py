from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException
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
    user_id: int | None = None,
    categories1: str = '',
    categories2: str = '',
    favorites_only: bool = False,
    price_min: int | None = None,
    price_max: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    cats1 = [c.strip() for c in categories1.split(',') if c.strip()]
    cats2 = [c.strip() for c in categories2.split(',') if c.strip()]
    finds = await crud.list_finds(db, cats1, cats2, price_min, price_max)
    fav_ids = set()
    if user_id:
        fav_ids = set(await crud.get_favorite_find_ids(db, user_id))
        if favorites_only:
            finds = [f for f in finds if f.id in fav_ids]
    result = []
    for f in finds:
        item = schemas.FindOut.model_validate(f)
        if user_id:
            item.is_favorite = f.id in fav_ids
        result.append(item)
    return result


@router.post('/finds/{find_id}/favorite')
async def toggle_favorite(find_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    user_id = data.get('user_id')
    if not user_id:
        raise HTTPException(status_code=400, detail='user_id required')
    favorite = await crud.toggle_favorite_find(db, user_id, find_id)
    return {'favorite': favorite}

