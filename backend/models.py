from sqlalchemy import Column, Integer, BigInteger, String, Date, Boolean, DateTime, JSON
from backend.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, index=True)
    agent_number = Column(String, unique=True, index=True)
    telegram_username = Column(String, index=True)
    join_date = Column(Date)
    location = Column(String)
    is_member = Column(Boolean, default=False)
    referrer_id = Column(BigInteger, index=True)


class Affiliate(Base):
    __tablename__ = 'affiliates'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, index=True)
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
    categories = Column(JSON)
    contact_link = Column(String)
    contact_phone = Column(String)
    contact_password = Column(String)


class FavoriteSupplier(Base):
    __tablename__ = 'favorite_suppliers'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, index=True)
    supplier_id = Column(Integer, index=True)


class FavoriteFind(Base):
    __tablename__ = 'favorite_finds'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, index=True)
    find_id = Column(Integer, index=True)


class Find(Base):
    __tablename__ = 'finds'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    photo_url = Column(String)
    product_url = Column(String)
    category = Column(String)
    brand = Column(String)
    price = Column(Integer)
    created_at = Column(DateTime)
    is_hot = Column(Boolean, default=False)
    is_new = Column(Boolean, default=False)
    is_high_margin = Column(Boolean, default=False)


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, index=True)
    months = Column(Integer)
    amount = Column(Integer)
    currency = Column(String)
    invoice_id = Column(String, index=True)
    status = Column(String)
    payment_url = Column(String)
