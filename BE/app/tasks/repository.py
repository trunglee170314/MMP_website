from typing import List, Optional
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models

class TaskRepository(Protocol):
    def create(self, title: str, user_id: int) -> models.Task: ...
    def get(self, task_id: int) -> Optional[models.Task]: ...
    def list_by_user(self, user_id: int) -> List[models.Task]: ...
    def save(self, task: models.Task) -> models.Task: ...
    def delete(self, task: models.Task) -> None: ...


class SqlAlchemyTaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, user_id: int) -> models.Task:
        t = models.Task(title=title, user_id=user_id)
        self.db.add(t)
        self.db.commit()
        self.db.refresh(t)
        return t

    def get(self, task_id: int) -> Optional[models.Task]:
        return self.db.get(models.Task, task_id)

    def list_by_user(self, user_id: int) -> List[models.Task]:
        stmt = select(models.Task).where(models.Task.user_id == user_id)
        return list(self.db.execute(stmt).scalars().all())

    def save(self, task: models.Task) -> models.Task:
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: models.Task) -> None:
        self.db.delete(task)
        self.db.commit()