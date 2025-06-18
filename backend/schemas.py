from pydantic import BaseModel
from datetime import date, datetime

class UserBase(BaseModel):
    agent_number: str
    join_date: date | None = None
    location: str | None = None

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    days_in_club: int | None = None
    status: str | None = None

    class Config:
        from_attributes = True
