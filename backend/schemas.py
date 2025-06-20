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
    is_member: bool | None = None

    model_config = {"from_attributes": True}


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

    model_config = {"from_attributes": True}


class SupplierBase(BaseModel):
    name: str
    description: str | None = None
    photo_url: str | None = None
    category1: str | None = None
    category2: str | None = None


class SupplierOut(SupplierBase):
    id: int
    is_favorite: bool | None = None

    model_config = {"from_attributes": True}


class SupplierContacts(BaseModel):
    contact_link: str | None = None
    contact_phone: str | None = None
    contact_password: str | None = None

    model_config = {"from_attributes": True}


class FindOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    photo_url: str | None = None
    price: int | None = None
    supplier_id: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
