from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..core.db import Base

class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    board_name = Column(String(255), nullable=False)
    barcode = Column(String(50), unique=True, nullable=False)
    ip = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", backref="boards")
    note = Column(String(1024), default="", nullable=True)
    status = Column(String(50), nullable=False)
    location = Column(String(512), default="", nullable=True)