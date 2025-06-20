import hashlib
import hmac
import json
import urllib.parse
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database import get_db
from backend.models import User
from backend.config import get_settings
from backend import crud
import time


router = APIRouter()


def check_telegram_auth(init_data: str, bot_token: str, max_age_sec: int = 86400) -> dict:
    """
    Проверка подписи и срока годности initData от Telegram Mini App.
    :param init_data: строка из window.Telegram.WebApp.initData
    :param bot_token: токен вашего Telegram-бота (строка)
    :param max_age_sec: максимальный возраст токена (по умолчанию 24ч)
    :return: dict с распарсенными данными Telegram-пользователя
    :raises: ValueError, если подпись невалидна или токен устарел
    """




    # 1. Парсим строку
    data = dict(urllib.parse.parse_qsl(init_data))
    hash_ = data.pop('hash', None)
    #data.pop('signature', None)

    # 2. Строим строку для подписи
    check_string = '\n'.join(f"{k}={v}" for k, v in sorted(data.items()))

    # 3. Ключ для подписи — HMAC-SHA256(bot_token, "WebAppData")
    secret_key = hmac.new(
        msg=bytes(bot_token, 'utf-8'),
        key=b'WebAppData',
        digestmod=hashlib.sha256
    ).digest()

    # 4. Считаем подпись для строки данных
    expected_hash = hmac.new(
        key=secret_key,
        msg=check_string.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    if expected_hash != hash_:
        print('Calculated:', expected_hash)
        print('Received:', hash_)
        print('Data check string:', check_string)
        print('BOT_TOKEN:', bot_token)
        print('secret_key (hex):', secret_key.hex())
        raise HTTPException(status_code=403, detail="Invalid Telegram WebApp initData signature")

    # 5. Проверка на актуальность токена
    if 'auth_date' in data and time.time() - int(data['auth_date']) > 86400:
        raise HTTPException(status_code=403, detail="InitData is outdated")

    return data


@router.post('/auth/telegram')
async def telegram_auth(request: Request, db: AsyncSession = Depends(get_db)):
    body = await request.json()
    print('RAW INITDATA:', body.get('initData'))
    init_data = body.get('initData')

    if not init_data:
        raise HTTPException(status_code=400, detail="initData required")
    bot_token = get_settings().TELEGRAM_BOT_TOKEN  # Добавь TELEGRAM_BOT_TOKEN в config

    user_data = check_telegram_auth(init_data, bot_token)
    user_json = user_data['user']
    user_obj = json.loads(user_json)
    user_id = int(user_obj['id'])
    first_name = user_obj.get('first_name', '')
    last_name = user_obj.get('last_name', '')
    username = user_obj.get('username', '')

    # Проверяем/создаём пользователя
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        ref_param = user_data.get('start_param')
        referrer_id = None
        if ref_param:
            try:
                referrer_id = crud.decode_referral(ref_param)
            except Exception:
                referrer_id = None
        user = await crud.create_user(
            db,
            user_id=user_id,
            agent_number=username,
            referrer_id=referrer_id,
        )
        await crud.create_affiliate(db, user.id)

    return {
        "id": user.id,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "is_member": user.is_member
    }

