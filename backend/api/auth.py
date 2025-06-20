import hashlib
import hmac
import urllib.parse
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from datetime import date
from backend.database import get_db
from backend.models import User
from backend.config import get_settings

router = APIRouter()


def check_telegram_auth(init_data: str, bot_token: str) -> dict:
    import urllib.parse
    import hmac
    import hashlib

    data = dict(urllib.parse.parse_qsl(init_data))
    hash_ = data.pop('hash', None)
    data.pop('signature', None)
    data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(data.items()))
    # ВНИМАНИЕ! Вот так:
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    if calculated_hash != hash_:
        print("Calculated:", calculated_hash)
        print("Received:", hash_)
        print("Data check string:", data_check_string)
        print("BOT_TOKEN:", bot_token)
        print("secret_key (hex):", secret_key.hex())
        raise HTTPException(status_code=403, detail="Invalid Telegram auth data")
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
