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


class AffiliateBase(BaseModel):
    user_id: int
    motivation: str | None = None
    share: int | None = None
    invited: int | None = None
    payments_sum: int | None = None
    earned: int | None = None
    paid: int | None = None
    balance: int | None = None
    referral_link: str | None = None
    materials_link: str | None = None
    withdraw_requested: bool | None = None


class AffiliateOut(AffiliateBase):
    id: int

    class Config:
        from_attributes = True
