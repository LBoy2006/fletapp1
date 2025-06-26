from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import httpx

from .. import crud, schemas
from ..database import get_db
from ..config import get_settings

router = APIRouter()


@router.post('/payments', response_model=schemas.PaymentOut)
async def create_invoice(data: schemas.PaymentCreate, db: AsyncSession = Depends(get_db)):
    settings = get_settings()
    amount_map = {1: 1990, 3: 4990, 6: 9990, 12: 19990}
    period_map = {
        1: 'MONTHLY',
        3: 'PERIOD_90_DAYS',
        6: 'PERIOD_180_DAYS',
        12: 'PERIOD_YEAR'
    }
    if data.months not in amount_map:
        raise HTTPException(status_code=400, detail='Invalid plan')
    amount = amount_map[data.months]
    payload = {
        "email": f"{data.user_id}@club.com",
        "offerId": settings.LAVA_OFFER_ID,
        "periodicity": period_map[data.months],
        "currency": "RUB",
        "buyerLanguage": "RU",
        "paymentMethod": "BANK131",
    }
    headers = {
        'accept': 'application/json',
        'X-Api-Key': settings.LAVA_API_KEY,
        'Content-Type': 'application/json',
    }
    invoice_id = str(uuid.uuid4())
    status = 'in-progress'
    pay_url = ''
    if not settings.TEST_MODE:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post('https://gate.lava.top/api/v2/invoice', json=payload, headers=headers)
            data_resp = resp.json()
            invoice_id = data_resp.get('id', invoice_id)
            status = data_resp.get('status', status)
            pay_url = data_resp.get('paymentUrl', '')
        except Exception:
            pass
    payment = await crud.create_payment(
        db,
        user_id=data.user_id,
        months=data.months,
        amount=amount,
        currency="RUB",
        invoice_id=invoice_id,
        status=status,
        payment_url=pay_url,
    )
    return payment
