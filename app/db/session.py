# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# .env에서 읽어온 DB URL
DATABASE_URL = settings.DATABASE_URL

# SQLAlchemy 엔진 생성 (Neon은 sslmode=require가 URL에 이미 포함돼 있음)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 끊어진 연결 미리 감지
)

# 세션 팩토리: 각 요청마다 SessionLocal() 해서 사용
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# FastAPI에서 의존성 주입으로 쓰는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
