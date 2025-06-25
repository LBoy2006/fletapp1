from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PaymentRequest(BaseModel):
    user_id: int
    months: int

class PaymentResponse(BaseModel):
    payment_url: str

@router.post('/payments/membership', response_model=PaymentResponse)
async def create_membership_payment(data: PaymentRequest):
    # In a real application this would create a payment in an external system
    url = f"https://pay.example.com/?user={data.user_id}&months={data.months}"
    return PaymentResponse(payment_url=url)
