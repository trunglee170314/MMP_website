from typing import Optional
from fastapi import HTTPException
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from .schemas import UserCreate
from . import models
from ..core import security

class UserRepository(Protocol):
    def get_by_email(self, email: str) -> Optional[models.User]: ...
    def create(self, payload: UserCreate, password_hash:str) -> models.User: ...
    def delete(self, user_id: int) -> bool: ...
    def approve_user(self, email: str) -> models.User: ...
    # def create_admin_if_not_exists(db: Session): ...

class SqlAlchemyUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_List_user(self) -> Optional[models.User]:
        stmt = select(models.User)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_email(self, email: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.email == email)
        return self.db.execute(stmt).scalars().first()

    def create(self, payload: UserCreate, password_hash:str) -> models.User:
        u = models.User(
            full_name=payload.full_name,
            user_name=payload.user_name,
            email=payload.email,
            code=payload.code,
            password_hash=password_hash,
            number_phone=payload.number_phone,
            role=payload.role or "user",
            auth_registered=False
        )

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

    # Approve registered user
    def approve_user(self, email: str) -> models.User:
        u = self.db.query(models.User).filter(models.User.email == email).first()
        if not u:
            raise HTTPException(status_code=404, detail="User not found")
        u.auth_registered = True
        self.db.commit()
        self.db.refresh(u)
        return u

    # def create_admin_if_not_exists(db: Session):
    #     admin_email = "Admin@gmail.com"
    #     admin_password = "admin"
    #     admin_user = db.query(models.User).filter(models.User.email == admin_email).first()
    #     if not admin_user:
    #         new_admin = models.User(
    #             email = admin_email,
    #             hashed_password = security.hash_password(admin_password),
    #             is_active = True,
    #             role = RoleEnum.admin,
    #             code = "123",
    #             number_phone = "",
    #             full_name = "system admin",
    #             is_active = True
    #         )

    #         db.add(new_admin)
    #         db.commit()
    #         db.refresh(new_admin)
    #         print(f"Admin account created: {admin_email}")
    #     else:
    #         print(f"Admin account already exists: {admin_email}")