from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from backend.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    agent_number = Column(String, unique=True, index=True)
    join_date = Column(Date)
    location = Column(String)
    is_member = Column(Boolean, default=False)
    referrer_id = Column(Integer, index=True)


class Affiliate(Base):
    __tablename__ = 'affiliates'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    motivation = Column(String)
    share = Column(Integer)
    invited = Column(Integer)
    payments_sum = Column(Integer)
    earned = Column(Integer)
    paid = Column(Integer)
    balance = Column(Integer)
    referral_link = Column(String)
    materials_link = Column(String)
    withdraw_requested = Column(Boolean, default=False)


class MotivationPhrase(Base):
    __tablename__ = 'motivation_phrases'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)


class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    photo_url = Column(String)
    category1 = Column(String)
    category2 = Column(String)
    contact_link = Column(String)
    contact_phone = Column(String)
    contact_password = Column(String)


class FavoriteSupplier(Base):
    __tablename__ = 'favorite_suppliers'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    supplier_id = Column(Integer, index=True)


class Find(Base):
    __tablename__ = 'finds'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    photo_url = Column(String)
    price = Column(Integer)
    supplier_id = Column(Integer, index=True)
    created_at = Column(DateTime)
