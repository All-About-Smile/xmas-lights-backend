# 📘 **🚀 FastAPI Time-Capsule Backend – Initial Setup Guide (Final README)**

이 문서는 **타임캡슐 서비스 백엔드(FastAPI 기반)**의
**초기 개발 환경 구축 단계 전체**를 정리한 공식 개발 문서입니다.

현재 단계는 *기능 구현 이전*이며,
프로젝트의 구조, DB 설정, 마이그레이션 환경, 및 코드 컨벤션 자동화 시스템까지 구성된 상태입니다.

---

# 📁 프로젝트 구조

```
backend/
 ├─ app/
 │   ├─ api/
 │   ├─ core/
 │   ├─ db/
 │   ├─ schemas/
 │   ├─ services/
 │   └── main.py
 ├─ alembic/
 ├─ alembic.ini
 ├─ .env
 ├─ requirements.txt
 └─ venv/
```

---

# 🧱 1. 개발 환경 세팅

```bash
python -m venv venv
venv\Scripts\activate
```

---

# 📦 2. 패키지 설치

```bash
pip install -r requirements.txt
```

---

# 🗄 3. 데이터베이스(Neon) 설정

Neon.tech PostgreSQL 사용.

| 항목            | 설정                           |
| --------------- | ------------------------------ |
| PostgreSQL 버전 | **17**                         |
| 클라우드        | **AWS**                        |
| 리전            | **Singapore (ap-southeast-1)** |

### ✔ .env / .env.dev / .env.local 예시

```
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require
SECRET_KEY=change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### ✔ Redis 및 Refresh Token 설정 예시

Refresh Token을 저장하기 위해 Redis Cloud를 사용하므로 다음 환경 변수를 함께 설정해야 한다.
```
REDIS_URL=redis://default:******@redis-11285.c9.us-east-1-2.ec2.cloud.redislabs.com:11285
REFRESH_TOKEN_EXPIRE_DAYS=7
```


※ `.env`와 `.env.*` 파일은 gitignore에 포함(비공개)

---

# 🧩 4. FastAPI 핵심 구성

- `config.py` – 환경변수 로드
- `security.py` – JWT 및 비밀번호 해싱
- `timecheck.py` – 날짜 계산 유틸

---

# 🗂 5. Schema (요청/응답 검증)

- auth_schema
- user_schema
- capsule_schema
- letter_schema
- public_schema

---

# 🧩 6. Service Layer

- auth_service
- capsule_service
- letter_service
- public_service

---

# 🗄 7. SQLAlchemy 설정

- `session.py`: SessionLocal / engine
- `base.py`: Base 클래스
- `models/`: ORM 모델 정의

관계 구조:

```
User (1) ─── (N) Letter
```

---

# 🏗 8. Alembic 마이그레이션

### ✔ 자동 생성

```bash
alembic revision --autogenerate -m "init tables"
```

### ✔ DB 최신 적용

```bash
alembic upgrade head
```

> ⚠ `alembic init` 은 최초 1회만 실행 (이미 생성되어 있음)

---

# 🔀 9. API 라우터

- /auth
- /capsule
- /letters
- /public

FastAPI main.py에서 include_router로 등록됨.

---

# 10. 서버 실행

## 로컬 테스트
### Window
```cmd
# 예시: set ENV={서버 환경 이름} && uvicorn app.main:app --reload
set ENV=local && uvicorn app.main:app --reload
```

### Linux
```bash
export ENV=local
uvicorn app.main:app --reload
```

## 운영 환경 (Linux)
### 방법
```bash
export ENV={환경이름}
gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  -w {워커 개수} \
  -b 0.0.0.0:8000
```

### 예시
```bash
export ENV=prod
gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  -w 3 \
  -b 0.0.0.0:8000
---

# 📘 11. Swagger / API 문서

문서:

- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

# ✨ 12. 코드 컨벤션 & 자동 검사 시스템

본 프로젝트는 아래 **Python 표준 개발 컨벤션**을 따릅니다:

- **Black**: 코드 자동 포매터
- **Ruff**: 린터 + import 정리
- **mypy**: 타입 검사
- **pre-commit**: git commit 시 자동 실행되는 검사 훅

### 🔧 개발자가 반드시 해야 할 초기 설정

레포를 처음 클론한 후 **최초 1회**:

```bash
pip install -r requirements.txt
pre-commit install
```

### 🔁 자동 검사 흐름

1. 파일 수정
2. 변경 파일 stage
3. commit 실행
4. pre-commit이 Black/Ruff 자동 실행
5. 문제가 없으면 커밋 성공
6. 문제가 있으면 수정 후 재커밋

Black 및 Ruff 설정은 `pyproject.toml`에서 관리됩니다.

---

# 🚫 13. .gitignore (필수)

다음 파일은 Git에 포함되지 않습니다:

- 가상환경(venv)
- `.env`
- pycache
- Alembic 캐시
- 로그 파일
- 로컬 DB 파일
- Docker 볼륨 데이터

공식 `.gitignore` 파일 전체는 다음과 같습니다:

```
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
# PostgreSQL (Local Volume)
# ================================
pgdata/
postgres/
postgres_data/
database/
db_data/

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

# ================================
# Logs / Temp
# ================================
*.tmp
*.log
*.out
*.bak

# ================================
# Python notebook
# ================================
.ipynb_checkpoints/

# ================================
# Ruff
# ================================
.ruff_cache/

# ================================
# Pre-commit
# ================================
.pre-commit/
```

---
