from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..core.db import Base

class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    board_name = Column(String(255), nullable=False)
    barcode = Column(Integer, unique=True, nullable=False)
    ip = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", backref="boards")
    note = Column(String(1024), default="", nullable=True)
    status = Column(String(50), nullable=False)
    location = Column(String(512), default="", nullable=True)