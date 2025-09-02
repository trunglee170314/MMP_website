from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Enum, func
from sqlalchemy.orm import relationship
from ..core.db import Base

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_task_id = Column(Integer, ForeignKey("type_tasks.id"))
    status = Column(String(50))
    description = Column(Text, nullable=True)
    priority = Column(String(50))
    pic_id = Column(Integer, ForeignKey("users.id"))
    classify = Column(String(50))
    start_date = Column(DateTime, default=func.now())
    due_date = Column(DateTime, nullable=True)
    redmine = Column(String(100))
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=True)
    note = Column(Text, nullable=True)
    score = Column(Integer)
    approve_status = Column(Boolean, default=False)

    type_task = relationship("TypeTask", back_populates="tasks")
    pic = relationship("User", back_populates="tasks")
    board = relationship("Board", back_populates="tasks")