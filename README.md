
# 📘 **🚀 FastAPI Time-Capsule Backend – Initial Setup Guide (Final README)**

이 문서는 **타임캡슐 서비스 백엔드(FastAPI 기반)**의
**초기 개발 환경 구축 과정 전체**를 정리한 공식 개발 문서입니다.

현재 단계는 *기능 구현 이전* 단계이며,
프로젝트의 전체 구조, 환경 설정, DB 기반, 그리고 마이그레이션 환경까지 모두 설정된 상태입니다.


---

# 📁 프로젝트 구조

```
backend/
 ├─ app/
 │   ├─ api/
 │   │    ├── auth.py
 │   │    ├── capsule.py
 │   │    ├── letters.py
 │   │    └── public.py
 │   ├─ core/
 │   │    ├── config.py
 │   │    ├── security.py
 │   │    └── timecheck.py
 │   ├─ db/
 │   │    ├── base.py
 │   │    ├── session.py
 │   │    └── models/
 │   │         ├── user.py
 │   │         ├── capsule.py
 │   │         └── letter.py
 │   ├── schemas/
 │   │    ├── auth_schema.py
 │   │    ├── user_schema.py
 │   │    ├── capsule_schema.py
 │   │    ├── letter_schema.py
 │   │    └── public_schema.py
 │   ├── services/
 │   │    ├── auth_service.py
 │   │    ├── capsule_service.py
 │   │    ├── letter_service.py
 │   │    └── public_service.py
 │   └── main.py
 ├─ alembic/
 ├─ alembic.ini
 ├─ .env
 ├─ requirements.txt
 └─ venv/
```

---

# 🧱 1. 개발 환경 세팅

## ✔ 가상환경 생성 & 활성화

```
python -m venv venv
venv\Scripts\activate
```

---

# 📦 2. 패키지 설치 (requirements.txt 기반)


다른 개발자(또는 새로운 환경)는 다음 명령어 하나로 **전체 패키지 설치**만 하면 됩니다:

```
pip install -r requirements.txt
```

---

# 🔐 3. 환경변수(.env) 설정

루트에 `.env` 파일 생성:

```
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require

SECRET_KEY=change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

`.env` 파일은 보안 파일이므로 **gitignore로 제외**합니다.

---

# ⚙️ 4. core 설정 (FastAPI 핵심 구성)

### ✔ config.py

* pydantic-settings v2 기반
* 모든 환경변수(.env) 로드
* settings 객체 제공

### ✔ security.py

* bcrypt 비밀번호 해싱
* JWT 토큰 생성(JOSE 라이브러리 기반)

### ✔ timecheck.py

* 타임캡슐 오픈 날짜 계산 유틸

---

# 🧩 5. 스키마(Schemas) 작성

FastAPI는 스키마(Pydantic 모델) 기반으로:

* 요청 데이터 검증
* 응답 데이터 구조
* Swagger 문서 자동 생성

을 수행합니다.

작성된 스키마:

* auth_schema.py
* user_schema.py
* capsule_schema.py
* letter_schema.py
* public_schema.py

---

# 🗂 6. 서비스 레이어(Service Layer)

서비스 레이어는 **비즈니스 로직을 담당하는 계층**이며,
현재는 함수 구조만 정의된 상태입니다.

* auth_service
* capsule_service
* letter_service
* public_service

구체적인 기능 구현은 이후 단계에서 진행합니다.

---

# 🗄 7. 데이터베이스 설정 (SQLAlchemy)

### ✔ base.py

SQLAlchemy Base 선언

### ✔ session.py

* engine
* SessionLocal
* get_db 의존성

Neon PostgreSQL 과 연결하도록 구성됨.

---

# 🏷 8. 모델(ORM) 정의

관계 구조:

```
User (1) ─── (1) Capsule ─── (N) Letter
```

모델 파일:

* user.py
* capsule.py
* letter.py

ORM 기반으로 모델과 관계가 정의되어 있으며
Alembic 마이그레이션을 통해 DB 테이블로 변환됩니다.

---

# 🏗 9. Alembic 마이그레이션 설정

Alembic은 SQLAlchemy 모델을 기반으로 DB 스키마를 자동 관리해주는 도구입니다.

---

## ✔ Alembic 설치

(이미 requirements.txt 에 포함됨)

```bash
pip install -r requirements.txt
```

---

## ✔ Alembic 초기화 (최초 1회만 실행)

※ 이미 프로젝트에 포함되어 있으므로 다시 실행하면 안 됩니다.

```
alembic init alembic
```

---

## ✔ 자동 마이그레이션 생성

모델을 기반으로 마이그레이션 파일 생성:

```
alembic revision --autogenerate -m "init tables"
```

---

## ✔ DB에 적용 (모든 개발자 공통)

프로젝트 clone 한 개발자는 **이 명령어 하나만 실행하면 DB 최신 상태가 됨:**

```
alembic upgrade head
```

> ⚠️ `alembic init` 은 절대 다시 하지 않는다 (초기 1회만).

---

# 🔀 10. API 라우터 구조 구성

각 라우터는 현재 “ping 테스트 엔드포인트”만 포함된 상태이며,
향후 기능 구현 시 서비스 레이어와 연결될 예정입니다.

* /auth
* /capsule
* /letters
* /public

FastAPI main.py에서 include_router로 등록됨.

---

# 📘 11. Swagger / API 문서

FastAPI는 스키마와 라우터를 기반으로
자동 API 문서를 생성하며, UI로 테스트가 가능합니다.

서버 실행:

```
uvicorn app.main:app --reload
```

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc 문서:

```
http://localhost:8000/redoc
```

Swagger 기능:

* 모든 endpoint 자동 나열
* 요청/응답 스키마 표시
* 직접 API 테스트
* Bearer Token 인증 테스트 가능

---

# 🚫 12. .gitignore 설명 (필수 항목 포함)

다음 파일들은 절대 git에 포함되면 안 됩니다:

### ❌ 가상환경 (venv)

### ❌ 환경변수(.env)

### ❌ DB 로컬 파일

### ❌ Alembic 캐시

### ❌ Docker 볼륨 데이터

### ❌ **pycache**

프로젝트에서 사용하는 공식 `.gitignore`는 다음과 같습니다:

```gitignore
# ================================
# Python
# ================================
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.pkl
.Python
*.so

# ================================
# Virtual Environment
# ================================
env/
venv/
ENV/
.venv/

# ================================
# FastAPI / Uvicorn logs
# ================================
logs/
*.log

# ================================
# Environment Variables
# ================================
.env
.env.*
!.env.example

# ================================
# IDE / Editor
# ================================
.vscode/
.idea/
*.swp

# ================================
# Pytest / Coverage
# ================================
.pytest_cache/
.coverage
htmlcov/
coverage.xml

# ================================
# MyPy / Type Checking
# ================================
.mypy_cache/
.dmypy.json
dmypy.json

# ================================
# Byte-compiled / Cache
# ================================
*.egg-info/
.eggs/
*.egg
*.manifest
*.spec
.cache/
*.cache/

# ================================
# Build / Distribution
# ================================
build/
dist/
pip-wheel-metadata/
*.whl

# ================================
# Docker
# ================================
*.pid
*.tar
docker-compose.override.yml

# Docker local volume data
data/
docker-data/
pgdata/
postgres/
postgres_data/
database/
db_data/

# ================================
# OS Specific
# ================================
.DS_Store
Thumbs.db

# ================================
# Local Database Files (SQLite)
# ================================
*.db
*.sqlite
*.sqlite3

# ================================
# Alembic
# ================================
alembic/versions/*.pyc
alembic/versions/__pycache__/
alembic/__pycache__/

# ================================
# Render / Deployment
# ================================
render.yaml
```

---

