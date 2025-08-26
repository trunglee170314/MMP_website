from typing import Optional

from . import models
from .schemas import InUserCreate, InUserUpdate
from .repository import UserRepository
from ..core import security
from ..core.config import settings

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    # helpers
    def _found_user(self, u: models.User) -> models.User:
        if not u:
            raise ValueError("User not found")
        return u

    def _ensure_unique(self, email: str, user_name: str) -> None:
        if self.repo.get_by_email(email):
            raise ValueError("Email already existed")
        if self.repo.get_by_user(user_name):
            raise ValueError("User name already existed")

    # actions
    def register(self, payload: InUserCreate) -> models.User:
        self._ensure_unique(payload.email, payload.user_name)
        return self.repo.create(payload, security.hash_password(payload.password))

    def authenticate(self, email: str, raw_password: str) -> Optional[models.User]:
        user = self.repo.get_by_email(email)
        if not user or not security.verify_password(raw_password, user.password_hash):
            raise ValueError("Invalid email or password")
        if not user.auth_registered:
            raise ValueError("User account not approved yet")
        return user

    def get_list_appr_user(self) -> Optional[models.User]:
        return self.repo.get_list_appr_user()

    def list_waiting_approve(self) -> Optional[models.User]:
        return self.repo.list_waiting_approve()

    def approve_user(self, user_id: int) -> Optional[models.User]:
        return self._found_user(self.repo.approve_user(user_id))

    def update_role(self, user_id: int, new_role: str) -> Optional[models.User]:
        return self.repo.update_role(user_id, new_role)

    def update_user(self, payload: InUserUpdate) -> Optional[models.User]:
        return self._found_user(self.repo.update_user(payload))

    def get_user_by_id(self, user_id: int) -> Optional[models.User]:
        return self._found_user(self.repo.get_by_id(user_id))

    def reset_password(self, user_id: int) -> Optional[models.User]:
        user = self._found_user(self.repo.get_by_id(user_id))
        if user.auth_registered == False:
            raise ValueError("User account not approved yet")

        hashed_pw = security.hash_password(settings.default_pw)

        return self.repo.update_password(user_id, hashed_pw)

    def delete_user(self, user_id: str) -> bool:
        return self.repo.delete_by_id(user_id)