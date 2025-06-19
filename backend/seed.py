from datetime import date
from .database import engine, SessionLocal
from .models import User, Affiliate, Supplier, Find, Base

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    user = db.query(User).first()
    if not user:
        user = User(
            agent_number='chn_098',
            join_date=date(2024, 1, 1),
            location='Москва',
            telegram_id=123,
            subscription_active=True,
        )
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
    if not db.query(Supplier).first():
        suppliers = [
            Supplier(
                name='Store A',
                description='Надежный поставщик техники',
                photo_url='https://via.placeholder.com/100',
                category1='техника',
                category2='Apple',
                contact_link='https://example.com',
                contact_phone='+1 111 111',
                contact_password='1234'
            ),
            Supplier(
                name='Fashion B',
                description='Модная одежда',
                photo_url='https://via.placeholder.com/100',
                category1='одежда',
                category2='LV',
                contact_link='https://example.com',
                contact_phone='+1 222 222',
                contact_password='abcd'
            )
        ]
        db.add_all(suppliers)
        db.commit()
    if not db.query(Find).first():
        finds = [
            Find(
                name='iPhone 15 Pro',
                description='Флагманский смартфон 2024 года',
                photo_url='https://via.placeholder.com/300',
                price=150000,
                supplier_id=1,
                created_at=date(2024, 6, 1)
            ),
            Find(
                name='Кроссовки Limited',
                description='Редкая модель',
                photo_url='https://via.placeholder.com/300',
                price=25000,
                supplier_id=2,
                created_at=date(2024, 5, 28)
            )
        ]
        db.add_all(finds)
        db.commit()
    db.close()

if __name__ == '__main__':
    seed()
