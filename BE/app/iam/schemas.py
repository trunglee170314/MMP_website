from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from ..core.Enum.roles_enum import RoleEnum


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    code: str
    number_phone: str
    full_name: str
    role: Optional[str] = RoleEnum.user


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    email: EmailStr
    full_name: str
    number_phone: str
    role: str
    is_active: bool


class LoginInput(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"