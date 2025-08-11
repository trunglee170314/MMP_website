# Users & Tasks API — FastAPI + SQLite (DDD-lite)

## Reuirements:
- Python 3.8.10
- Ubuntu (already has `python3.8-venv`, `pip`)

## Structure:
    BE/
    ├─ app/
    │  ├─ main.py              # Start project
    │  ├─ core/
    │  │  ├─ config.py         # Manage environment variable
    │  │  ├─ db.py             # Init and connect DB
    │  │  └─ security.py       # Verify security
    │  ├─ iam/                 # Identity & Access Management
    │  │  ├─ models.py         # ORM model
    │  │  ├─ schemas.py        # Pydantic schemas
    │  │  ├─ repository.py     # CRUD
    │  │  ├─ service.py        # Logic layer
    │  │  ├─ deps.py           # Session (user's information after login)
    │  │  └─ api.py            # Controller (Communicate with front-end)
    │  └─ tasks/
    │     ├─ models.py
    │     ├─ schemas.py
    │     ├─ repository.py
    │     ├─ service.py
    │     └─ api.py
    ├─ .env                    # Private environment
    ├─ requirements.txt        # libs requirement
    └─ README.md

## Install:
```bash
python3.8 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
uvicorn app.main:app --reload
```
