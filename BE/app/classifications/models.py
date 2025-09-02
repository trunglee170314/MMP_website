from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from ..core.db import Base

class Classification(Base):
    __tablename__ = "classifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(225), nullable=False)
    description = Column(Text, nullable=True)

    tasks = relationship("Task", back_populates="classification")