from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from database.db import Base 

class User(Base):
    __tablename__ = "users"

    name = Column(String, unique=True, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
