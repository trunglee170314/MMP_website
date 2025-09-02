from typing import Optional
from .schemas import task_create, task_update, task_claim
from .repository import TaskRepository
from . import models

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def get_list_task(self) -> Optional[models.Task]:
        return self.repo.get_list_task()
    
    def get_list_task_waiting_appr(self) -> Optional[models.Task]:
        return self.repo.get_list_task_waiting_appr()
    
    def get_task_id(self, task_id: int) -> Optional[models.Task]:
        return self.repo.get_task_by_id(task_id)

    def update_task(self, task_id: int, task_update: task_update) -> Optional[models.Task]:
        return self.repo.update_task(task_id, task_update)
    
    def task_claim(self, task_id: int, task_claim: task_claim) -> Optional[models.Task]:
        return self.repo.update_task_claim(task_id, task_claim)
    
    def update_complete_task(self, task_id: int) -> Optional[models.Task]:
        return self.repo.update_complete_task(task_id)
    
    def create_task(self, payload: task_create) -> Optional[models.Task]:
        return self.repo.create_task(payload)
    
    def approve_task(self, task_id: int) -> Optional[models.Task]:
        return self.repo.approve_task(task_id)
    
    def resolved_task(self, task_id: int) -> Optional[models.Task]:
        return self.repo.resolved_task(task_id)
    
    def delete_task(self, task_id: int) -> bool:
        return self.repo.delete_task(task_id)