from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .association import user_board
from ..core.db import Base
from ..utilities.common_enums import RoleEnum
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__  = "users"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, nullable=False)
    full_name = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    number_phone = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    auth_registered = Column(Boolean, default=True, nullable=False)
    role = Column(String(50), default=RoleEnum.user, nullable=False)

    boards = relationship("Board", secondary=user_board, back_populates="owners")
    tasks = relationship("Task", back_populates="pic")