
from typing import Any, Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from ..core.Enum.roles_enum import RoleEnum

class HttpResponse(BaseModel):
    status: int
    message: str
    data: Optional[Any] = None

class UserCreate(BaseModel):
    email: EmailStr
    user_name: str
    password: str
    code: int
    number_phone: str
    full_name: str

class UserUpdate(BaseModel):
    full_name: str
    user_name: str
    email: EmailStr
    code: int
    password: Optional[str] = None
    number_phone: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: int
    user_name: str
    email: EmailStr
    full_name: str
    number_phone: str
    role: str
    auth_registered: bool


class LoginInput(BaseModel):
    email: EmailStr
    password: str