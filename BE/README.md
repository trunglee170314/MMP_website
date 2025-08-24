# MMP Management Website Backend APIs — FastAPI + SQLite (DDD-lite)

## Reuirements:
- Python 3.8.10
- Ubuntu (already has `python3.8-venv`, `pip`)

## Structure:
    BE/
    ├─ app/
    │  ├─ main.py
    │  ├─ core/
    │  │  ├─ config.py
    │  │  ├─ db.py
    │  │  └─ security.py
    │  ├─ iam/                  # User & Authentication (Identity and Access Management)
    │  │  ├─ models.py
    │  │  |─ association.py
    │  │  ├─ schemas.py
    │  │  ├─ repository.py
    │  │  ├─ service.py
    │  │  ├─ deps.py
    │  │  └─ api.py
    │  ├─ tasks/                # Task management
    │  │  ├─ models.py
    │  │  ├─ schemas.py
    │  │  ├─ repository.py
    │  │  ├─ service.py
    │  │  └─ api.py
    │  └─boards/                # Board management
    │     ├─ models.py
    │     ├─ schemas.py
    │     ├─ repository.py
    │     ├─ service.py
    │     └─ api.py
    ├─ .env
    ├─ requirements.txt
    └─ README.md

## Installation & Run:
### Create a virtual environment:
```bash
python3.8 -m venv .venv
```

### Activate it:
```bash
source .venv/bin/activate
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the development server:
```bash
uvicorn app.main:app --reload
```

## API Docs:
- Swagger UI → http://localhost:8000/docs
- ReDoc → http://localhost:8000/redoc
