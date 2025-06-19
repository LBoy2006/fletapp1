from fastapi import FastAPI, Depends, HTTPException
import hashlib
import hmac
import os
import json
import urllib.parse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS settings to allow requests from the frontend during development
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_telegram(init_data: str) -> dict:
    bot_token = os.environ.get('BOT_TOKEN', '')
    if not bot_token:
        raise HTTPException(status_code=500, detail='BOT_TOKEN not configured')
    data = urllib.parse.parse_qs(init_data)
    data = {k: v[0] for k, v in data.items()}
    hash_value = data.pop('hash', None)
    if not hash_value:
        raise HTTPException(status_code=400, detail='hash required')
    data_check = '\n'.join(f"{k}={data[k]}" for k in sorted(data))
    secret = hashlib.sha256(bot_token.encode()).digest()
    h = hmac.new(secret, data_check.encode(), hashlib.sha256).hexdigest()
    if h != hash_value:
        raise HTTPException(status_code=403, detail='Invalid hash')
    user_json = data.get('user')
    if not user_json:
        raise HTTPException(status_code=400, detail='user required')
    return json.loads(user_json)


@app.get('/users/{user_id}', response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    result = schemas.UserOut.model_validate(user)
    if user.join_date:
        result.days_in_club = (date.today() - user.join_date).days
    if result.days_in_club is not None:
        d = result.days_in_club
        if d < 30:
            result.status = 'Новичок'
        elif d < 180:
            result.status = 'Агент'
        elif d < 365:
            result.status = 'Партнёр'
        else:
            result.status = 'Ветеран'
    return result


@app.patch('/users/{user_id}', response_model=schemas.UserOut)
def update_user(user_id: int, data: schemas.UserBase, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if data.location is not None:
        user.location = data.location
    db.commit()
    db.refresh(user)
    return read_user(user_id, db)


@app.get('/affiliate/{user_id}', response_model=schemas.AffiliateOut)
def read_affiliate(user_id: int, db: Session = Depends(get_db)):
    stat = db.query(models.Affiliate).filter(models.Affiliate.user_id == user_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail='Stats not found')
    return stat


@app.post('/affiliate/{user_id}/withdraw', response_model=schemas.AffiliateOut)
def request_withdraw(user_id: int, db: Session = Depends(get_db)):
    stat = db.query(models.Affiliate).filter(models.Affiliate.user_id == user_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail='Stats not found')
    stat.withdraw_requested = True
    db.commit()
    db.refresh(stat)
    return stat


@app.get('/suppliers/categories1')
def get_categories1(db: Session = Depends(get_db)):
    cats = db.query(models.Supplier.category1).distinct().all()
    return [c[0] for c in cats if c[0]]


@app.get('/suppliers/categories2')
def get_categories2(categories1: str = '', db: Session = Depends(get_db)):
    q = db.query(models.Supplier.category2)
    if categories1:
        cats1 = [c.strip() for c in categories1.split(',') if c.strip()]
        q = q.filter(models.Supplier.category1.in_(cats1))
    cats = q.distinct().all()
    return [c[0] for c in cats if c[0]]


@app.get('/suppliers', response_model=list[schemas.SupplierOut])
def list_suppliers(user_id: int, categories1: str = '', categories2: str = '', favorites_only: bool = False, db: Session = Depends(get_db)):
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


@app.get('/suppliers/{supplier_id}/contacts', response_model=schemas.SupplierContacts)
def get_supplier_contacts(supplier_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not s:
        raise HTTPException(status_code=404, detail='Supplier not found')
    return schemas.SupplierContacts.model_validate(s)


@app.post('/suppliers/{supplier_id}/favorite')
def toggle_favorite(supplier_id: int, data: dict, db: Session = Depends(get_db)):
    user_id = data.get('user_id')
    if not user_id:
        raise HTTPException(status_code=400, detail='user_id required')
    fav = db.query(models.FavoriteSupplier).filter(models.FavoriteSupplier.user_id == user_id, models.FavoriteSupplier.supplier_id == supplier_id).first()
    if fav:
        db.delete(fav)
        db.commit()
        return {'favorite': False}
    else:
        fav = models.FavoriteSupplier(user_id=user_id, supplier_id=supplier_id)
        db.add(fav)
        db.commit()
        return {'favorite': True}


@app.get('/suppliers/{supplier_id}', response_model=schemas.SupplierOut)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not s:
        raise HTTPException(status_code=404, detail='Supplier not found')
    return schemas.SupplierOut.model_validate(s)


@app.get('/finds', response_model=list[schemas.FindOut])
def list_finds(db: Session = Depends(get_db)):
    items = db.query(models.Find).order_by(models.Find.created_at.desc()).all()
    return items


@app.post('/auth/telegram', response_model=schemas.AuthResult)
def auth_telegram(data: schemas.AuthRequest, db: Session = Depends(get_db)):
    user_data = verify_telegram(data.init_data)
    telegram_id = user_data.get('id')
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if user and user.subscription_active:
        result = schemas.UserOut.model_validate(user)
        if user.join_date:
            result.days_in_club = (date.today() - user.join_date).days
        return schemas.AuthResult(is_member=True, user=result)
    return schemas.AuthResult(is_member=False, user=None)


@app.post('/subscribe')
def subscribe(data: schemas.AuthRequest, db: Session = Depends(get_db)):
    user_data = verify_telegram(data.init_data)
    telegram_id = user_data.get('id')
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not user:
        user = models.User(
            agent_number=f"chn_{telegram_id}",
            join_date=date.today(),
            telegram_id=telegram_id,
            subscription_active=True,
        )
        db.add(user)
    else:
        user.subscription_active = True
        if not user.join_date:
            user.join_date = date.today()
    db.commit()
    return {"success": True}
