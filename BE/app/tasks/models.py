from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Enum, func
from sqlalchemy.orm import relationship
from ..utilities.common_enums import TaskStatusEnum, TaskPriorityEnum, TypeTaskEnum
from ..core.db import Base

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_task = Column(Enum(TypeTaskEnum), nullable=False)
    status = Column(Enum(TaskStatusEnum), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum(TaskPriorityEnum), nullable=True)
    pic_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    classification_id = Column(Integer, ForeignKey("classifications.id"))
    start_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    redmine = Column(Text, nullable=True)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=True)
    note = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)
    approve_status = Column(Boolean, default=False)

    classification = relationship("Classification", back_populates="tasks")
    pic = relationship("User", back_populates="tasks")
    board = relationship("Board", back_populates="tasks")