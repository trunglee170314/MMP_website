from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.db import Base, engine, get_db
from .core.config import settings
from .iam.api import router as iam_router
from .tasks.api import router as tasks_router
from .iam import models as iam_models  # noqa: F401 - ensure metadata is loaded
from .tasks import models as task_models  # noqa: F401 - ensure metadata is loaded
from .iam.repository import SqlAlchemyUserRepository

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Users & Tasks API")

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
    repo = SqlAlchemyUserRepository(db)  # truyền db vào
    repo.create_admin()  # không cần db nữa
    db.close()
    
app.include_router(iam_router)
app.include_router(tasks_router)
