from sqlalchemy import Column, Integer, String, Date, Boolean
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    agent_number = Column(String, unique=True, index=True)
    join_date = Column(Date)
    location = Column(String)


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
