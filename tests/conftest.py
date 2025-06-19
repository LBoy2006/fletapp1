import os
import sys
from datetime import date, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app
from backend import models
from backend.database import get_db


@pytest.fixture()
def client(tmp_path):
    db_path = tmp_path / 'test.db'
    engine = create_engine(f'sqlite:///{db_path}', connect_args={'check_same_thread': False})
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    models.Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.state.SessionLocal = TestingSessionLocal
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def db_session(client):
    SessionLocal = client.app.state.SessionLocal
    db = SessionLocal()
    user = models.User(agent_number='agent', join_date=date(2024, 1, 1), location='Moscow')
    db.add(user)
    db.commit()
    db.refresh(user)
    affiliate = models.Affiliate(user_id=user.id)
    supplier1 = models.Supplier(name='Store A', contact_link='link')
    supplier2 = models.Supplier(name='Store B', contact_link='link')
    find = models.Find(name='Item', supplier_id=1, created_at=datetime.utcnow())
    db.add_all([affiliate, supplier1, supplier2, find])
    db.commit()
    client.app.state.user_id = user.id
    try:
        yield db
    finally:
        db.close()
