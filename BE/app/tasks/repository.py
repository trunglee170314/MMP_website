from typing import List, Optional
from fastapi import HTTPException
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from . import models
from .schemas import task_claim, task_create, task_update
from typing import Optional
from fastapi import HTTPException, status

class TaskRepository(Protocol):
    def get_list_task(self) -> List[models.Task]: ...
    def get_list_task_appr(self) -> List[models.Task]: ...
    def get_task_by_id(self, task_id: int) -> Optional[models.Task]: ...
    def update_task(self, task_id: int, task_update: task_update) -> Optional[models.Task]: ...
    def update_task_claim(self, task_id: int, task_claim: task_claim) -> Optional[models.Task]: ...
    def update_complete_task(self, task_id: int) -> Optional[models.Task]: ...
    def create_task(self, payload: task_create) -> Optional[models.Task]: ...
    def approve_task(self, task_id: int) -> models.Task: ...
    def delete_task(self, task_id: int) -> bool: ...

class SqlAlchemyTaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_task(self) -> List[models.Task] :
        stmt = select(models.Task)
        return self.db.execute(stmt).scalars().all()
    
    def get_list_task_appr(self) -> List[models.Task]:
        stmt = select(models.Task).where(models.Task.approve_status == True)
        return self.db.execute(stmt).scalars().all()
    
    def approve_task(self, task_id: int) -> models.Task:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            return None
        task.approve_status = True
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_task_by_id(self, task_id: int) -> Optional[models.Task]:
        stmt = select(models.Task).where(models.Task.id == task_id)
        return self.db.execute(stmt).scalars().first()
    
    def update_task(self, task_id: int, task_update: task_update) -> Optional[models.Task]:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            return None
        
        task.type_task_id = task_update.type_task_id 
        task.board_id = task_update.board_id 
        task.pic_id = task_update.pic
        task.description = task_update.description
        task.priority = task_update.priority
        task.classify = task_update.classify
        task.redmine = task_update.redmine
        task.note = task_update.note
        task.score = task_update.score
        
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def update_task_claim(self, task_id: int, task_claim: task_claim) -> Optional[models.Task]:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            return None
        elif not task.approve_status:
            raise ValueError("Task is not approved")

        task.PIC = task_claim.pic
        task.status = task_claim.status

        self.db.commit()
        self.db.refresh(task)
        return task
    
    def update_complete_task(self, task_id: int) -> Optional[models.Task]:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            raise ValueError("Task is not found")
        elif not task.approve_status:
            raise ValueError("Task is not approved")
        
        task.status = "Reviewing"
        task.due_date = datetime.now()
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def create_task(self, payload: task_create) -> Optional[models.Task]:
        task = models.Task(
            type_task_id = payload.type_task_id,
            board_id = payload.board_id,
            status = payload.status,
            description = payload.description,
            priority = payload.priority,
            pic_id = payload.pic_id,
            classify = payload.classify,
            start_date = payload.start_date,
            due_date = payload.due_date,
            redmine = payload.redmine,
            note = payload.note,
            score  = payload.score
        )

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete_task(self, task_id: int) -> bool:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            return False
        
        self.db.delete(taks)
        self.db.commit()
        return True
