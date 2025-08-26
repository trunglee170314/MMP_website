from typing import Optional, List
from fastapi import HTTPException
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from .schemas import UserCreate, UserUpdate
from . import models
from ..core.Enum.roles_enum import RoleEnum
from ..core import security

class UserRepository(Protocol):
    def get_by_email(self, email: str) -> Optional[models.User]: ...
    def create(self, payload: UserCreate, password_hash:str) -> models.User: ...
    def delete(self, user_id: int) -> bool: ...
    def approve_user(self, user_id: int) -> models.User: ...
    def list_waiting_approve(self) -> List[models.User]: ...
    def update_role(self, user_id: int, new_role: str) -> Optional[models.User]: ...
    def update_password(self, user_id: int, hashed_pw: str) -> Optional[models.User]: ...
    def update_user(self, payload: UserUpdate) -> Optional[models.User]: ...
    def get_by_id(self, user_id: int) -> Optional[models.User]: ...
    def get_list_user(self) -> List[models.User]: ...
    def create_admin(self): ...

class SqlAlchemyUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list_user(self) -> List[models.User]:
        stmt = select(models.User)
        return self.db.execute(stmt).scalars().all()

    def get_by_email(self, email: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.email == email)
        return self.db.execute(stmt).scalars().first()
    
    def get_by_id(self, user_id: int) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.id == user_id)
        return self.db.execute(stmt).scalars().first()

    def create(self, payload: UserCreate, password_hash:str) -> models.User:
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
    
    def delete(self, user_id: int) -> bool:
        u = self.db.get(models.User, user_id)
        if not u:
            return False
        self.db.delete(u)
        self.db.commit()
        return True
    
    # Approve registered user
    def approve_user(self, user_id: int) -> models.User:
        u = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not u:
            raise HTTPException(status_code=404, detail="User not found")
        u.auth_registered = True
        self.db.commit()
        self.db.refresh(u)
        return u
    
    def list_waiting_approve(self) -> List[models.User]:
        stmt = select(models.User).where(models.User.auth_registered == False)
        result = self.db.execute(stmt).scalars().all()
        return result
    
    def update_role(self, user_id: int, new_role: str) -> Optional[models.User]:
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        print(user)
        if not user:
            return None
        user.role = new_role
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, payload: UserUpdate) -> Optional[models.User]:
        user = self.db.query(models.User).filter(models.User.email == payload.email).first()
        
        if not user:
            return None
        
        user.full_name = payload.full_name
        user.user_name = payload.user_name
        user.email = payload.email
        user.code = payload.code
        user.number_phone = payload.number_phone

        if payload.password:
            user.password_hash = security.hash_password(payload.password)

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
    
    def create_admin(self):
        admin_user = self.db.query(models.User).filter(models.User.email == "admin@gmail.com").first()
        if not admin_user:
            new_admin = models.User( 
                email="admin@gmail.com",
                password_hash=security.hash_password("admin"),
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