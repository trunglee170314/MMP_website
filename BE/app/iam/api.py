from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..core.security import create_access_token
from .schemas import UserCreate, UserOut, LoginInput, Token
from .repository import SqlAlchemyUserRepository
from .service import UserService
from .deps import get_current_user, require_admin

router = APIRouter(prefix="", tags=["iam"])