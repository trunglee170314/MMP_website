from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Optional
from .repository import SqlAlchemyUserRepository
from .service import UserService
from ..core.db import get_db
from ..core.security import decode_token
from . import models
from ..utilities.role_name_enum import RoleEnum

#HTTPBearer
bearer_scheme = HTTPBearer()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(SqlAlchemyUserRepository(db))

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    svc: UserService = Depends(get_user_service),
) -> models.User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = decode_token(token)
        sub: Optional[str] = payload.get("sub")
        if sub is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    user = svc.repo.get_by_email(sub)
    if user is None or not user.auth_registered:
        raise credentials_exc
    return user

def require_admin(current_user: models.User = Depends(get_current_user)) -> models.User:
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
    return current_user

def require_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    return current_user
