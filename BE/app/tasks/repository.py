from typing import List, Optional
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models

class TaskRepository(Protocol):
    pass


class SqlAlchemyTaskRepository:
    pass