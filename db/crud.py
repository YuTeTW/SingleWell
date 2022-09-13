from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .models import User
from .database import Base, engine
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UnicornException(Exception):
    def __init__(self, name: str, status_code: int, description):
        self.name = name
        self.status_code = status_code
        self.description = description


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email, password):
    try:
        user_db = User(email=email, password=pwd_context.hash(password))
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=create_user.__name__, description=str(e), status_code=500)
    return user_db


def reset_password(db: Session, email, new_password):
    user_db = db.query(User).filter(User.email == email).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="user not exist")
    try:
        hashed_password = pwd_context.hash(new_password)
        user_db.password = hashed_password
        user_db.updated_at = datetime.now()
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=reset_password.__name__, description=str(e), status_code=500)
    return user_db




def delete_all_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
