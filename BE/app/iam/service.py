from typing import Optional
from .schemas import UserCreate
from .repository import UserRepository
from . import models
from ..core import security

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, payload: UserCreate) -> models.User:
        if self.repo.get_by_email(payload.email):
            raise ValueError("Email already registered")
        hashed = security.hash_password(payload.password)
    
        return self.repo.create(payload, hashed)

    def authenticate(self, email: str, raw_password: str) -> Optional[models.User]:
        user = self.repo.get_by_email(email)
        if not user:
            return None
        if not security.verify_password(raw_password, user.password_hash):
            return None
        if not user.is_active:
            return None
        return user