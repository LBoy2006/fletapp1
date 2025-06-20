from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/suppliers/categories1')
async def get_categories1(db: AsyncSession = Depends(get_db)):
    return await crud.list_categories1(db)


@router.get('/suppliers/categories2')
async def get_categories2(categories1: str = '', db: AsyncSession = Depends(get_db)):
    cats1 = [c.strip() for c in categories1.split(',') if c.strip()]
    return await crud.list_categories2(db, cats1)


@router.get('/suppliers', response_model=list[schemas.SupplierOut])
async def list_suppliers(
    user_id: int,
    categories1: str = '',
    categories2: str = '',
    favorites_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    cats1 = [c.strip() for c in categories1.split(',') if c.strip()]
    cats2 = [c.strip() for c in categories2.split(',') if c.strip()]
    suppliers = await crud.list_suppliers(db, cats1, cats2)
    fav_ids = set(await crud.get_favorite_supplier_ids(db, user_id))
    if favorites_only:
        suppliers = [s for s in suppliers if s.id in fav_ids]
    result = []
    for s in suppliers:
        item = schemas.SupplierOut.model_validate(s)
        item.is_favorite = s.id in fav_ids
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
    return schemas.SupplierOut.model_validate(s)

