from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    nickname = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 한 유저 = 하나의 캡슐 (1:1)
    capsule = relationship(
        "Capsule",
        back_populates="owner",
        uselist=False     # ⭐ 핵심 → 1:1 관계 설정
    )
