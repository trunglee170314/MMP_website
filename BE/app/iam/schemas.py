from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    full_name: str
    user_name: str
    email: EmailStr
    code: str
    password: str
    number_phone: str
    role: Optional[str] = "user"

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    email: EmailStr
    full_name: str
    number_phone: str
    role: str
    auth_registered: bool


class LoginInput(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"