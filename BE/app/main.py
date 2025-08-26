from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.db import Base, engine, get_db
from .core.config import settings
from .iam.api import router as iam_router
from .iam import models as iam_models  # noqa: F401 - ensure metadata is loaded
from .iam.repository import SqlAlchemyUserRepository

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MMP management website backend APIs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    db = next(get_db())  # sync generator
    repo = SqlAlchemyUserRepository(db)
    repo.create_admin()
    db.close()

app.include_router(iam_router)