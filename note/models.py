from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    String,
    TIMESTAMP,
    text,
)
from database.engine import Base
from sqlalchemy.orm import relationship


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable = False
    )
    owner_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    owner = relationship("User", back_populates = "notes")
