from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from ..core.db import Base

class TypeTask(Base):
    __tablename__ = "type_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_task_name = Column(String(225), nullable=False)
    description = Column(Text, nullable=True)

    tasks = relationship("Task", back_populates="type_task")