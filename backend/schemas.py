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
    categories: list[str] | None = None


class SupplierOut(SupplierBase):
    id: int
    is_favorite: bool | None = None
    favorites_count: int | None = None

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
    product_url: str | None = None
    category: str | None = None
    brand: str | None = None
    price: int | None = None
    created_at: datetime
    is_favorite: bool | None = None
    favorites_count: int | None = None
    is_hot: bool | None = None
    is_new: bool | None = None
    is_high_margin: bool | None = None

    model_config = {"from_attributes": True}


class PaymentCreate(BaseModel):
    user_id: int
    months: int


class PaymentOut(BaseModel):
    id: int
    user_id: int
    months: int
    amount: int
    currency: str
    invoice_id: str | None = None
    status: str | None = None
    payment_url: str | None = None

    model_config = {"from_attributes": True}
