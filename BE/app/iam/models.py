from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..core.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="user", nullable=False)  # "admin" hoặc "user"
    is_active = Column(Boolean, default=True, nullable=False)

    # relationship ở phía Task sẽ khai báo back_populates="owner"