from typing import Optional
from .repository import TaskRepository
from . import models

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, user_id: int, title: str) -> models.Task:
        return self.repo.create(title=title, user_id=user_id)

    def update_task(self, user_id: int, task_id: int, *, title: Optional[str] = None, done: Optional[bool] = None) -> models.Task:
        t = self.repo.get(task_id)
        if not t or t.user_id != user_id:
            raise ValueError("Task not found")
        if title is not None:
            t.title = title
        if done is not None:
            t.done = done
        return self.repo.save(t)

    def delete_task(self, user_id: int, task_id: int) -> None:
        t = self.repo.get(task_id)
        if not t or t.user_id != user_id:
            raise ValueError("Task not found")
        self.repo.delete(t)