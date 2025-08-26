from typing import Optional
from .schemas import UserCreate, UserUpdate
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
        if not user.auth_registered:
            return None
        return user
    
    def get_list_user(self) -> Optional[models.User]:
        return self.repo.get_list_user()

    def list_waiting_approve(self) -> Optional[models.User]:
        return self.repo.list_waiting_approve()
    
    def approve_user(self, user_id: int) -> Optional[models.User]:
        return self.repo.approve_user(user_id)

    def update_role(self, user_id: int, new_role: str) -> Optional[models.User]:
        return self.repo.update_role(user_id, new_role)
    
    def update_user(self, payload: UserUpdate) -> Optional[models.User]:
        return self.repo.update_user(payload)
    
    def get_user_by_id(self, user_id: int) -> Optional[models.User]:
        return self.repo.get_by_id(user_id)
    
    def reset_password(self, user_id: int, pass_word: str) -> Optional[models.User]:
        user = self.repo.get_by_id(user_id)
        if not user:
            return None
        
        hashed_pw = security.hash_password(pass_word)
        self.repo.update_password(user_id, hashed_pw)
        return user

    def delete_user(self, user_id: str) -> str:
        try:
            deleted = self.repo.delete(user_id)
            if deleted:
                return "User deleted successfully."
            else:
                return "User not found or could not be deleted."
        except Exception as e:
            return f"Failed to delete user: {str(e)}"
        