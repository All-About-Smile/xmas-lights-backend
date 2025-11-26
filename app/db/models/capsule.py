from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Capsule(Base):
    __tablename__ = "capsules"

    id = Column(Integer, primary_key=True, index=True)

    # 유저 1명당 캡슐 1개 → owner_id 에 unique=True 적용
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    open_at = Column(DateTime(timezone=True), nullable=False)
    is_public = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # User ↔ Capsule (1:1)
    owner = relationship("User", back_populates="capsule")

    # Capsule → Letters (1:N)
    letters = relationship("Letter", back_populates="capsule")
