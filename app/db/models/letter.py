from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Letter(Base):
    __tablename__ = "letters"

    id = Column(Integer, primary_key=True, index=True)

    capsule_id = Column(Integer, ForeignKey("capsules.id"), nullable=False)
    writer_name = Column(String, nullable=False)
    content = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 1:N
    capsule = relationship("Capsule", back_populates="letters")
