from typing import List, Optional
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models
from .schemas import TypeTaskCreateUpdate


class TypeTaskRepository(Protocol):
    def get_list_type_task(self) -> List[models.TypeTask]: ...
    def get_type_task_by_id(self, type_task_id: int) -> Optional[models.TypeTask]: ...
    def create_type_task(self, payload: TypeTaskCreateUpdate) -> models.TypeTask: ...
    def update_type_task(self, type_task_id: int, payload: TypeTaskCreateUpdate) -> Optional[models.TypeTask]: ...
    def delete_type_task(self, type_task_id: int) -> bool: ...


class SqlAlchemyTypeTaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_type_task(self) -> List[models.TypeTask]:
        stmt = select(models.TypeTask)
        return self.db.execute(stmt).scalars().all()
    
    def get_type_task_by_id(self, type_task_id: int) -> Optional[models.TypeTask]:
        stmt = select(models.TypeTask).where(models.TypeTask.id == type_task_id)
        return self.db.execute(stmt).scalars().first()
    
    def create_type_task(self, payload: TypeTaskCreateUpdate) -> models.TypeTask:
        type_task = models.TypeTask(
            type_task_name = payload.name,
            description = payload.description
        )
        self.db.add(type_task)
        self.db.commit()
        self.db.refresh(type_task)
        return type_task
    
    def update_type_task(self, type_task_id: int, payload: TypeTaskCreateUpdate) -> Optional[models.TypeTask]:
        type_task = self.db.query(models.TypeTask).filter(models.TypeTask.id == type_task_id).first()
        if not type_task:
            return None
        
        type_task.type_task_name = payload.name
        type_task.description = payload.description
        
        self.db.commit()
        self.db.refresh(type_task)
        return type_task
    
    def delete_type_task(self, type_task_id: int) -> bool:
        type_task = self.db.query(models.TypeTask).filter(models.TypeTask.id == type_task_id).first()
        if not type_task:
            return False
        
        self.db.delete(type_task)
        self.db.commit()
        return True
