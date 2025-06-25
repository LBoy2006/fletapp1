from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/finds/categories')
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await crud.list_find_categories(db)


@router.get('/finds/brands')
async def get_brands(categories: str = '', db: AsyncSession = Depends(get_db)):
    cats = [c.strip() for c in categories.split(',') if c.strip()]
    return await crud.list_find_brands(db, cats)


@router.get('/finds', response_model=list[schemas.FindOut])
async def list_finds(
    user_id: int | None = None,
    favorites_only: bool = False,
    db: AsyncSession = Depends(get_db)
):
    finds = await crud.list_finds(db)
    fav_ids = set()
    fav_counts = await crud.get_all_find_favorites_count(db)
    if user_id:
        fav_ids = set(await crud.get_favorite_find_ids(db, user_id))
        if favorites_only:
            finds = [f for f in finds if f.id in fav_ids]
    result = []
    for f in finds:
        item = schemas.FindOut.model_validate(f)
        if user_id:
            item.is_favorite = f.id in fav_ids
        item.favorites_count = fav_counts.get(f.id, 0)
        result.append(item)
    return result


@router.post('/finds/{find_id}/favorite')
async def toggle_favorite(find_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    user_id = data.get('user_id')
    if not user_id:
        raise HTTPException(status_code=400, detail='user_id required')
    favorite = await crud.toggle_favorite_find(db, user_id, find_id)
    return {'favorite': favorite}

