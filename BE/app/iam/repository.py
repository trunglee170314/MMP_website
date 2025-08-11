from typing import Optional
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models

class UserRepository(Protocol):
    pass

class SqlAlchemyUserRepository:
    pass