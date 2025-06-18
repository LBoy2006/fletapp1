from datetime import date
from .database import engine, SessionLocal
from .models import User, Base

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    if not db.query(User).first():
        user = User(agent_number='chn_089', join_date=date(2022,1,1), location='Москва')
        db.add(user)
        db.commit()
    db.close()

if __name__ == '__main__':
    seed()
