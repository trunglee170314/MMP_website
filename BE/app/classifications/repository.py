from typing import List, Optional
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models
from .schemas import ClassificationCreateUpdate
from typing import List, Optional, Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models
from .schemas import ClassificationCreateUpdate


class ClassificationRepository(Protocol):
    def get_list(self) -> List[models.Classification]: ...
    def get_by_id(self, classification_id: int) -> Optional[models.Classification]: ...
    def create(self, payload: ClassificationCreateUpdate) -> models.Classification: ...
    def update(self, classification_id: int, payload: ClassificationCreateUpdate) -> Optional[models.Classification]: ...
    def delete(self, classification_id: int) -> bool: ...


class SqlAlchemyClassificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list(self) -> List[models.Classification]:
        stmt = select(models.Classification)
        return self.db.execute(stmt).scalars().all()

    def get_by_id(self, classification_id: int) -> Optional[models.Classification]:
        classification = self.db.query(models.Classification).filter(models.Classification.id == classification_id).first()
        if not classification :
            ValueError(f"Classification with id {classification_id} was not found")
        return classification

    def create(self, payload: ClassificationCreateUpdate) -> models.Classification:
        classification  = models.Classification(
            name=payload.name,
            description=payload.description
        )
        self.db.add(classification)
        self.db.commit()
        self.db.refresh(classification)
        return classification

    def update(
        self, classification_id: int, payload: ClassificationCreateUpdate
    ) -> Optional[models.Classification]:
        classification  = self.get_by_id(classification_id)
        if not classification :
            raise ValueError(f"Classification with id {classification_id} was not found")
        classification.name = payload.name
        classification.description = payload.description
        self.db.commit()
        self.db.refresh(classification)
        return classification

    def delete(self, classification_id: int) -> bool:
        classification = self.get_by_id(classification_id)
        if not classification:
            raise ValueError(f"Classification with id {classification_id} was not found")
        self.db.delete(classification)
        self.db.commit()
        return True
