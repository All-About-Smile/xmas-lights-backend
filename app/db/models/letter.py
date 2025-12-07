from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Letter(Base):
    __tablename__ = "letters"

    id = Column(Integer, primary_key=True, index=True)

    # FK: 어떤 사용자(작성자)가 쓴 편지인지
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 편지 번호 (예: 1번, 2번, 3번 편지)
    letter_number = Column(Integer, nullable=False)

    # 롤링페이퍼에 보여줄 닉네임
    writer_nickname = Column(String(50), nullable=False)

    # 편지 내용
    content = Column(Text, nullable=False)

    # 장식 종류 (예: "star", "bell", "candy")
    ornament_type = Column(String(50), nullable=False)

    # 작성 시간
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Soft delete
    is_deleted = Column(Boolean, default=False)

    # 수정 시 필요한 비밀번호
    password_for_edit = Column(String(255), nullable=True)

    # User 관계 (1:N)
    user = relationship("User", back_populates="letters")
