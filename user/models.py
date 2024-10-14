from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from database.engine import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone = True), server_default = text("now()"), nullable=False
    )
    notes = relationship("Note", back_populates = "owner")
