from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, index=True, default=datetime.now())
    updated_at = Column(DateTime, index=True, default=datetime.now())
