import datetime as dt
from typing import Optional
from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from .config import settings
from pydantic import BaseModel

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

def hash_password(raw: str) -> str:
    return pwd_ctx.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    return pwd_ctx.verify(raw, hashed)

def create_access_token(data: dict, expires_minutes: Optional[int] = None) -> dict:
    expire_minutes = expires_minutes or settings.access_token_expire_minutes
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    return {"access_token": jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM), "expire": expire}

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
