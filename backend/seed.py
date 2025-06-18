from datetime import date
from .database import engine, SessionLocal
from .models import User, Affiliate, Base

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    user = db.query(User).first()
    if not user:
        user = User(agent_number='chn_098', join_date=date(2024,1,1), location='Москва')
        db.add(user)
        db.commit()
    if not db.query(Affiliate).filter(Affiliate.user_id == user.id).first():
        stat = Affiliate(
            user_id=user.id,
            motivation='Время привлекать новобранцев',
            share=10,
            invited=3,
            payments_sum=10000,
            earned=1000,
            paid=500,
            balance=6000,
            referral_link='https://t.me/club_bot?start=ref123',
            materials_link='https://drive.google.com/folder'
        )
        db.add(stat)
        db.commit()
    db.close()

if __name__ == '__main__':
    seed()
