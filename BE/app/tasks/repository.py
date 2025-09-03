from typing import List, Optional
from fastapi import HTTPException
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from ..utilities.common_enums import TaskStatusEnum
from . import models
from .schemas import task_claim, task_create, task_update
from typing import Optional
from ..iam.models import User

class TaskRepository(Protocol):
    def get_list_task(self) -> List[models.Task]: ...
    def get_list_task_waiting_appr(self) -> List[models.Task]: ...
    def get_task_by_id(self, task_id: int) -> Optional[models.Task]: ...
    def update_task(self, task_id: int, task_update: task_update) -> Optional[models.Task]: ...
    def update_task_claim(self, task_id: int, task_claim: task_claim) -> Optional[models.Task]: ...
    def update_complete_task(self, task_id: int) -> Optional[models.Task]: ...
    def create_task(self, payload: task_create) -> Optional[models.Task]: ...
    def approve_task(self, task_id: int) -> models.Task: ...
    def resolved_task(self, task_id: int) -> models.Task: ...
    def delete_task(self, task_id: int) -> bool: ...

class SqlAlchemyTaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_task(self) -> List[models.Task] :
        stmt = select(models.Task)
        return self.db.execute(stmt).scalars().all()

    def get_list_task_waiting_appr(self) -> List[models.Task]:
        stmt = select(models.Task).where(models.Task.approve_status == False)
        return self.db.execute(stmt).scalars().all()

    def approve_task(self, task_id: int) -> models.Task:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        task.approve_status = True
        self.db.commit()
        self.db.refresh(task)
        return task

    def resolved_task(self, task_id: int) -> models.Task:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task with id {task_id} not found")

        task.status = TaskStatusEnum.RESOLVED
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task_by_id(self, task_id: int) -> Optional[models.Task]:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        return task

    def update_task(self, task_id: int, task_update: task_update) -> Optional[models.Task]:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task with id {task_id} not found")

        task.type_task = task_update.type
        task.board_id = task_update.board_id
        task.pic_id = task_update.pic_id
        task.description = task_update.description
        task.priority = task_update.priority
        task.classification_id = task_update.classication_id
        task.redmine = task_update.redmine
        task.note = task_update.note
        task.score = task_update.score
        task.start_date = task_update.start_date
        task.due_date = task_update.due_date
        task.status = task_update.status

        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task_claim(self, task_id: int, task_claim: task_claim) -> Optional[models.Task]:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        # Validate task
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        elif not task.approve_status:
            raise ValueError("Task is not approved")

        # Validate PIC
        if task_claim.pic is not None:
            user = self.db.query(User).filter(User.id == task_claim.pic).first()
            if not user:
                raise ValueError(f"User with id {task_claim.pic} not found")

        task.pic_id = task_claim.pic
        task.status = TaskStatusEnum.ON_GOING

        self.db.commit()
        self.db.refresh(task)
        return task

    def update_complete_task(self, task_id: int) -> Optional[models.Task]:
        task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            raise ValueError("Task is not found")
        elif not task.approve_status:
            raise ValueError("Task is not approved")

        task.status = TaskStatusEnum.ON_REVIEWING
        self.db.commit()
        self.db.refresh(task)
        return task

    def create_task(self, payload: task_create) -> Optional[models.Task]:
        task = models.Task(
            type_task = payload.type,
            board_id = payload.board_id,
            status = TaskStatusEnum.FREE,
            description = payload.description,
            priority = payload.priority,
            pic_id = payload.pic_id,
            classification_id = payload.classication_id,
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
            raise ValueError(f"Task with id {task_id} not found")

        self.db.delete(task)
        self.db.commit()
        return True