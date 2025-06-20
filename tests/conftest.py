import os
import sys
from datetime import date, datetime

import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app
from backend import models
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
            user = models.User(agent_number='agent', join_date=date(2024, 1, 1), location='Moscow')
            db.add(user)
            await db.commit()
            await db.refresh(user)
            affiliate = models.Affiliate(user_id=user.id)
            supplier1 = models.Supplier(name='Store A', contact_link='link')
            supplier2 = models.Supplier(name='Store B', contact_link='link')
            find = models.Find(name='Item', supplier_id=1, created_at=datetime.utcnow())
            db.add_all([affiliate, supplier1, supplier2, find])
            await db.commit()
            client.app.state.user_id = user.id

    asyncio.get_event_loop().run_until_complete(seed_data())
    yield
