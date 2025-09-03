from typing import Optional, List
from .schemas import ClassificationCreateUpdate
from .repository import ClassificationRepository
from . import models

class ClassificationService:
    def __init__(self, repo: ClassificationRepository):
        self.repo = repo

    def get_list_classification(self) -> List[models.Classification]:
        return self.repo.get_list()

    def get_classification_by_id(self, classification_id: int) -> Optional[models.Classification]:
        return self.repo.get_by_id(classification_id)

    def create_classification(self, payload: ClassificationCreateUpdate) -> models.Classification:
        return self.repo.create(payload)

    def update_classification(self, classification_id: int, payload: ClassificationCreateUpdate) -> Optional[models.Classification]:
        return self.repo.update(classification_id, payload)

    def delete_classification(self, classification_id: int) -> bool:
        return self.repo.delete(classification_id)