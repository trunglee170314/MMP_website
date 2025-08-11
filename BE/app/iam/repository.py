from typing import Optional
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models

class UserRepository(Protocol):
    def get_by_email(self, email: str) -> Optional[models.User]: ...
    def create(self, email: str, password_hash: str, role: str = "user") -> models.User: ...
    def delete(self, user_id: int) -> bool: ...


class SqlAlchemyUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, email: str, password_hash: str, role: str = "user") -> models.User:
        u = models.User(email=email, password_hash=password_hash, role=role)
        self.db.add(u)
        self.db.commit()
        self.db.refresh(u)
        return u

    def delete(self, user_id: int) -> bool:
        u = self.db.get(models.User, user_id)
        if not u:
            return False
        self.db.delete(u)
        self.db.commit()
        return True