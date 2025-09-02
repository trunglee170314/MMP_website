from typing import Any, Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean
from datetime import datetime


class TypeTaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type_task_name: str
    description: str

class TypeTaskCreateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None