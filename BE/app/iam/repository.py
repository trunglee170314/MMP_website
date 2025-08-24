from typing import Optional, List, Iterable
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from .schemas import InUserCreate, InUserUpdate
from . import models
from ..utilities.role_name_enum import RoleEnum
from ..core import security

class UserRepository(Protocol):
    def get_by_email(self, email: str) -> Optional[models.User]: ...
    def create(self, payload: InUserCreate, password_hash:str) -> models.User: ...
    def delete_by_id(self, user_id: int) -> bool: ...
    def approve_user(self, user_id: int) -> models.User: ...
    def list_waiting_approve(self) -> List[models.User]: ...
    def update_role(self, user_id: int, new_role: str) -> Optional[models.User]: ...
    def update_password(self, user_id: int, hashed_pw: str) -> Optional[models.User]: ...
    def update_user(self, payload: InUserUpdate) -> Optional[models.User]: ...
    def get_by_id(self, user_id: int) -> Optional[models.User]: ...
    def get_by_ids(self, user_ids: Iterable[int]) -> List[models.User]: ...
    def get_list_appr_user(self) -> List[models.User]: ...
    def create_admin(self): ...

class SqlAlchemyUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_appr_user(self) -> List[models.User]:
        stmt = select(models.User).where(models.User.auth_registered == True)
        return self.db.execute(stmt).scalars().all()

    def get_by_email(self, email: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.email == email)
        return self.db.execute(stmt).scalars().first()

    def get_by_user(self, user_name: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.user_name == user_name)
        return self.db.execute(stmt).scalars().first()

    def get_by_id(self, user_id: int) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.id == user_id)
        user = self.db.execute(stmt).scalars().first()
        if not user:
            return None
        return user

    def get_by_ids(self, user_ids: Iterable[int]) -> List[models.User]:
        if not user_ids:
            return []
        return self.db.scalars(select(models.User).where(models.User.id.in_(user_ids))).all()

    def create(self, payload: InUserCreate, password_hash:str) -> models.User:
        u = models.User(
            email=payload.email,
            password_hash=password_hash,
            role=RoleEnum.user,
            code=payload.code,
            user_name=payload.user_name,
            number_phone=payload.number_phone,
            full_name=payload.full_name,
            auth_registered=False
        )

        self.db.add(u)
        self.db.commit()
        self.db.refresh(u)
        return u

    def delete_by_id(self, user_id: int) -> bool:
        user = self.db.get(models.User, user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    def approve_user(self, user_id: int) -> models.User:
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return None
        user.auth_registered = True
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_waiting_approve(self) -> List[models.User]:
        stmt = select(models.User).where(models.User.auth_registered == False)
        return self.db.execute(stmt).scalars().all()

    def update_role(self, user_id: int, new_role: str) -> Optional[models.User]:
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return None
        user.role = new_role
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, payload: InUserUpdate) -> Optional[models.User]:
        user = self.db.query(models.User).filter(models.User.email == payload.email).first()
        if not user:
            return None

        data = payload.dict(exclude_unset=True)

        pw = data.pop("password", None)
        if pw:
            user.password_hash = security.hash_password(payload.password)

        for field, value in data.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def update_password(self, user_id: int, hashed_pw: str) -> Optional[models.User]:
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            user.password_hash = hashed_pw
            self.db.commit()
            self.db.refresh(user)
            return user
        return None

    # Debug only
    def create_admin(self):
        admin_user = self.db.query(models.User).filter(models.User.email == "admin@example.com").first()
        if not admin_user:
            new_admin = models.User(
                email="admin@example.com",
                password_hash=security.hash_password("Pass1234"),
                role=RoleEnum.admin,
                code=1,
                user_name="admin",
                number_phone="099999999",
                full_name="System admin",
                auth_registered=True
            )

            self.db.add(new_admin)
            self.db.commit()
            self.db.refresh(new_admin)
        else:
            None