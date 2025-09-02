from typing import Optional, List
from .schemas import TypeTaskCreateUpdate
from .repository import TypeTaskRepository
from . import models

class TypeTaskService:
    def __init__(self, repo: TypeTaskRepository):
        self.repo = repo

    def get_list_type_task(self) -> List[models.TypeTask]:
        return self.repo.get_list_type_task()

    def get_type_task_by_id(self, type_task_id: int) -> Optional[models.TypeTask]:
        return self.repo.get_type_task_by_id(type_task_id)

    def create_type_task(self, payload: TypeTaskCreateUpdate) -> models.TypeTask:
        return self.repo.create_type_task(payload)

    def update_type_task(self, type_task_id: int, payload: TypeTaskCreateUpdate) -> Optional[models.TypeTask]:
        return self.repo.update_type_task(type_task_id, payload)

    def delete_type_task(self, type_task_id: int) -> bool:
        return self.repo.delete_type_task(type_task_id)
