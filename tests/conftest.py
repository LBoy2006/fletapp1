import os
import sys
from datetime import date, datetime

import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app
from backend import models, crud
from backend.database import get_db


@pytest.fixture()
def client(tmp_path):
    db_path = tmp_path / 'test.db'
    engine = create_async_engine(f'sqlite+aiosqlite:///{db_path}')
    TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)

    asyncio.get_event_loop().run_until_complete(init_models())

    async def override_get_db():
        async with TestingSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    app.state.SessionLocal = TestingSessionLocal
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def db_session(client):
    SessionLocal = client.app.state.SessionLocal

    async def seed_data():
        async with SessionLocal() as db:
            phrase = models.MotivationPhrase(text='Join us now!')
            db.add(phrase)
            await db.commit()
            user = models.User(
                id=1000000000000,
                agent_number='agent',
                telegram_username='test_user',
                join_date=date(2024, 1, 1),
                location='Moscow'
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            await crud.create_affiliate(db, user.id)
            supplier1 = models.Supplier(name='Store A', contact_link='link', categories=['CatA', 'CatB'])
            supplier2 = models.Supplier(name='Store B', contact_link='link', categories=['CatB'])
            find1 = models.Find(
                name='Item 1',
                product_url='http://example.com/item1',
                category='CatA', brand='BrandX',
                price=100,
                created_at=datetime.utcnow()
            )
            find2 = models.Find(
                name='Item 2',
                product_url='http://example.com/item2',
                category='CatB', brand='BrandY',
                price=200,
                created_at=datetime.utcnow()
            )
            db.add_all([supplier1, supplier2, find1, find2])
            await db.commit()
            client.app.state.user_id = user.id

    asyncio.get_event_loop().run_until_complete(seed_data())
    yield
