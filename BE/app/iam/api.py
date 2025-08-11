from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..core.security import create_access_token
from .schemas import UserCreate, UserOut, LoginInput, Token
from .repository import SqlAlchemyUserRepository
from .service import UserService
from .deps import get_current_user, require_admin

router = APIRouter(prefix="", tags=["iam"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(SqlAlchemyUserRepository(db))


@router.post("/auth/register", response_model=UserOut)
def register(payload: UserCreate, svc: UserService = Depends(get_user_service)):
    try:
        u = svc.register(payload.email, payload.password, payload.role)
        return u
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/login", response_model=Token)
def login(payload: LoginInput, svc: UserService = Depends(get_user_service)):
    user = svc.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users", response_model=list[UserOut], dependencies=[Depends(require_admin)])
def list_users(db: Session = Depends(get_db)):
    repo = SqlAlchemyUserRepository(db)
    # simple listing without pagination
    from sqlalchemy import select
    from . import models

    return list(db.execute(select(models.User)).scalars().all())


@router.delete("/users/{user_id}", dependencies=[Depends(require_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    repo = SqlAlchemyUserRepository(db)
    ok = repo.delete(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}