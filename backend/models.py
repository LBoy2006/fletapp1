from sqlalchemy import Column, Integer, String, Date
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    agent_number = Column(String, unique=True, index=True)
    join_date = Column(Date)
    location = Column(String)
