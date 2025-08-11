from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from .repository import SqlAlchemyUserRepository
from .service import UserService
from ..core.db import get_db
from ..core.security import decode_token
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")