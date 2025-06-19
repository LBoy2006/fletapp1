from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/suppliers/categories1')
def get_categories1(db: Session = Depends(get_db)):
    cats = db.query(models.Supplier.category1).distinct().all()
    return [c[0] for c in cats if c[0]]


@router.get('/suppliers/categories2')
def get_categories2(categories1: str = '', db: Session = Depends(get_db)):
    q = db.query(models.Supplier.category2)
    if categories1:
        cats1 = [c.strip() for c in categories1.split(',') if c.strip()]
        q = q.filter(models.Supplier.category1.in_(cats1))
    cats = q.distinct().all()
    return [c[0] for c in cats if c[0]]


@router.get('/suppliers', response_model=list[schemas.SupplierOut])
def list_suppliers(
    user_id: int,
    categories1: str = '',
    categories2: str = '',
    favorites_only: bool = False,
    db: Session = Depends(get_db),
):
    q = db.query(models.Supplier)
    if categories1:
        cats1 = [c.strip() for c in categories1.split(',') if c.strip()]
        q = q.filter(models.Supplier.category1.in_(cats1))
    if categories2:
        cats2 = [c.strip() for c in categories2.split(',') if c.strip()]
        q = q.filter(models.Supplier.category2.in_(cats2))
    suppliers = q.all()
    fav_ids = set(
        r.supplier_id for r in db.query(models.FavoriteSupplier).filter(models.FavoriteSupplier.user_id == user_id)
    )
    if favorites_only:
        suppliers = [s for s in suppliers if s.id in fav_ids]
    result = []
    for s in suppliers:
        item = schemas.SupplierOut.model_validate(s)
        item.is_favorite = s.id in fav_ids
        result.append(item)
    return result


@router.get('/suppliers/{supplier_id}/contacts', response_model=schemas.SupplierContacts)
def get_supplier_contacts(supplier_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not s:
        raise HTTPException(status_code=404, detail='Supplier not found')
    return schemas.SupplierContacts.model_validate(s)


@router.post('/suppliers/{supplier_id}/favorite')
def toggle_favorite(supplier_id: int, data: dict, db: Session = Depends(get_db)):
    user_id = data.get('user_id')
    if not user_id:
        raise HTTPException(status_code=400, detail='user_id required')
    fav = db.query(models.FavoriteSupplier).filter(
        models.FavoriteSupplier.user_id == user_id,
        models.FavoriteSupplier.supplier_id == supplier_id,
    ).first()
    if fav:
        db.delete(fav)
        db.commit()
        return {'favorite': False}
    else:
        fav = models.FavoriteSupplier(user_id=user_id, supplier_id=supplier_id)
        db.add(fav)
        db.commit()
        return {'favorite': True}


@router.get('/suppliers/{supplier_id}', response_model=schemas.SupplierOut)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not s:
        raise HTTPException(status_code=404, detail='Supplier not found')
    return schemas.SupplierOut.model_validate(s)
