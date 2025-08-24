from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..core.db import Base
from ..core.Enum.roles_enum import RoleEnum

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default=RoleEnum.user, nullable=False)  # "admin" hoặc "user"
    code = Column(String(100), nullable=False)
    number_phone = Column(String(100), nullable=True)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)