from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Index, Integer,
                        String, Text, UniqueConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Letter(Base):
    __tablename__ = "letters"

    id = Column(Integer, primary_key=True, index=True)

    # FK: 롤링페이퍼의 주인 (편지를 받는 사용자)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 롤링페이퍼 내 편지 순서
    letter_number = Column(Integer, nullable=False)

    # 작성자 닉네임 (비로그인)
    writer_nickname = Column(String(50), nullable=False)

    # 편지 내용
    content = Column(Text, nullable=False)

    # 오너먼트 (일반)
    ornament_shape = Column(String(20), nullable=False)
    ornament_color = Column(String(20), nullable=False)

    # 이벤트 오너먼트 여부
    is_event_ornament = Column(Boolean, server_default="false", nullable=False)

    # 작성 시간
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Soft delete
    is_deleted = Column(Boolean, server_default="false", nullable=False)

    # 편지 수정용 비밀번호 (hash 저장 전제)
    password_for_edit = Column(String(255), nullable=True)

    # 관계 설정
    user = relationship("User", back_populates="letters")

    __table_args__ = (
        # 롤링페이퍼 내 편지 번호 유니크 보장
        UniqueConstraint("user_id", "letter_number", name="uq_user_letter_number"),

        # 롤링페이퍼 조회 성능 최적화
        Index("idx_letters_user_id_created_at", "user_id", "created_at"),
    )
