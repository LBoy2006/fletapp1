from datetime import date
import asyncio
from sqlalchemy import select

from backend.database import engine, SessionLocal
from backend.models import (
    User,
    Affiliate,
    Supplier,
    Find,
    MotivationPhrase,
    Base,
)
from backend.crud import create_affiliate

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed():
    await create_tables()
    async with SessionLocal() as db:
        user = await db.get(User, 1)
        if not user:
            user = User(agent_number='chn_098', join_date=date(2024, 1, 1), location='Москва')
            db.add(user)
            await db.commit()
            await db.refresh(user)

        result = await db.execute(select(MotivationPhrase))
        if not result.scalar_one_or_none():
            phrases = [
                MotivationPhrase(text='Время привлекать новобранцев'),
                MotivationPhrase(text='Твои рекруты ждут тебя!'),
            ]
            db.add_all(phrases)
            await db.commit()

        result = await db.execute(select(Affiliate).where(Affiliate.user_id == user.id))
        if not result.scalar_one_or_none():
            await create_affiliate(db, user.id)

        result = await db.execute(select(Supplier))
        if not result.scalar_one_or_none():
            suppliers = [
                Supplier(
                    name='Store A',
                    description='Надежный поставщик техники',
                    photo_url='https://via.placeholder.com/100',
                    category1='техника',
                    category2='Apple',
                    contact_link='https://example.com',
                    contact_phone='+1 111 111',
                    contact_password='1234',
                ),
                Supplier(
                    name='Fashion B',
                    description='Модная одежда',
                    photo_url='https://via.placeholder.com/100',
                    category1='одежда',
                    category2='LV',
                    contact_link='https://example.com',
                    contact_phone='+1 222 222',
                    contact_password='abcd',
                ),
            ]
            db.add_all(suppliers)
            await db.commit()

        result = await db.execute(select(Find))
        if not result.scalar_one_or_none():
            finds = [
                Find(
                    name='iPhone 15 Pro',
                    description='Флагманский смартфон 2024 года',
                    photo_url='https://via.placeholder.com/300',
                    price=150000,
                    supplier_id=1,
                    created_at=date(2024, 6, 1),
                ),
                Find(
                    name='Кроссовки Limited',
                    description='Редкая модель',
                    photo_url='https://via.placeholder.com/300',
                    price=25000,
                    supplier_id=2,
                    created_at=date(2024, 5, 28),
                ),
            ]
            db.add_all(finds)
            await db.commit()

if __name__ == '__main__':
    asyncio.run(seed())

