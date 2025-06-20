import hashlib
import hmac
import urllib.parse
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from datetime import date
from backend.database import get_db
from backend.models import User
from backend.config import get_settings
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
    # Парсим строку запроса
    data = dict(urllib.parse.parse_qsl(init_data))
    hash_ = data.pop('hash', None)
    data.pop('signature', None)  # Telegram иногда добавляет signature - убираем

    # Собираем строку для подписи
    check_string = '\n'.join(f"{k}={v}" for k, v in sorted(data.items()))

    # Ключ для подписи — по документации Mini App!
    secret_key = hmac.new(
        msg=bot_token.encode('utf-8'),
        key=b'WebAppData',
        digestmod=hashlib.sha256
    ).digest()

    # Проверяем подпись
    expected_hash = hmac.new(secret_key, check_string.encode('utf-8'), hashlib.sha256).hexdigest()
    if expected_hash != hash_:
        print('Calculated:', expected_hash)
        print('Received:', hash_)
        print('Data check string:', check_string)
        print('BOT_TOKEN:', bot_token)
        print('secret_key (hex):', secret_key.hex())
        raise HTTPException(status_code=403, detail="Invalid Telegram WebApp initData signature")

    # Проверяем свежесть данных (24 часа — стандарт Telegram)
    if 'auth_date' in data:
        if time.time() - int(data['auth_date']) > max_age_sec:
            raise ValueError("Telegram WebApp initData expired")

    return data







@router.post('/auth/telegram')
async def telegram_auth(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    print('RAW INITDATA:', body.get('initData'))
    init_data = body.get('initData')

    if not init_data:
        raise HTTPException(status_code=400, detail="initData required")
    bot_token = get_settings().TELEGRAM_BOT_TOKEN  # Добавь TELEGRAM_BOT_TOKEN в config

    user_data = check_telegram_auth(init_data, bot_token)
    user_id = int(user_data['user[id]'])
    first_name = user_data.get('user[first_name]', '')
    last_name = user_data.get('user[last_name]', '')
    username = user_data.get('user[username]', '')

    # Проверяем/создаём пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(
            id=user_id,
            agent_number=username,
            join_date=date.today(),
            location=''
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return {
        "id": user.id,
        "first_name": first_name,
        "last_name": last_name,
        "username": username
    }
