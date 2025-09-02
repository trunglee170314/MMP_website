from typing import Any, Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from ..utilities.role_name_enum import RoleEnum
from datetime import datetime

class OutToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expire: datetime

class InUserCreate(BaseModel):
    email: EmailStr
    user_name: str
    password: str
    code: int
    number_phone: str
    full_name: str

class InUserUpdate(BaseModel):
    full_name: str
    user_name: str
    email: EmailStr
    code: Optional[int] = None
    password: str
    number_phone: Optional[str] = None

class OutUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: int
    user_name: str
    email: EmailStr
    full_name: str
    number_phone: str
    role: str

class InLogin(BaseModel):
    email: EmailStr
    password: str