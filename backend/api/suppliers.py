from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/suppliers/categories')
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await crud.list_categories(db)




@router.get('/suppliers', response_model=list[schemas.SupplierOut])
async def list_suppliers(
    user_id: int,
    categories: str = '',
    favorites_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    cats = [c.strip() for c in categories.split(',') if c.strip()]
    suppliers = await crud.list_suppliers(db, cats)
    fav_ids = set(await crud.get_favorite_supplier_ids(db, user_id))
    fav_counts = await crud.get_all_favorites_count(db)
    if favorites_only:
        suppliers = [s for s in suppliers if s.id in fav_ids]
    result = []
    for s in suppliers:
        item = schemas.SupplierOut.model_validate(s)
        item.is_favorite = s.id in fav_ids
        item.favorites_count = fav_counts.get(s.id, 0)
        result.append(item)
    return result


@router.get('/suppliers/{supplier_id}/contacts', response_model=schemas.SupplierContacts)
async def get_supplier_contacts(supplier_id: int, db: AsyncSession = Depends(get_db)):
    s = await crud.get_supplier(db, supplier_id)
    if not s:
        raise HTTPException(status_code=404, detail='Supplier not found')
    return schemas.SupplierContacts.model_validate(s)


@router.post('/suppliers/{supplier_id}/favorite')
async def toggle_favorite(supplier_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    user_id = data.get('user_id')
    if not user_id:
        raise HTTPException(status_code=400, detail='user_id required')
    favorite = await crud.toggle_favorite_supplier(db, user_id, supplier_id)
    return {'favorite': favorite}


@router.get('/suppliers/{supplier_id}', response_model=schemas.SupplierOut)
async def get_supplier(supplier_id: int, db: AsyncSession = Depends(get_db)):
    s = await crud.get_supplier(db, supplier_id)
    if not s:
        raise HTTPException(status_code=404, detail='Supplier not found')
    item = schemas.SupplierOut.model_validate(s)
    item.favorites_count = await crud.get_supplier_favorites_count(db, supplier_id)
    return item

