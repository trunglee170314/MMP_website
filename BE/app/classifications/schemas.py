from typing import Any, Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean
from datetime import datetime

class ClassificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str

class ClassificationCreateUpdate(BaseModel):
    name: str
    description: Optional[str] = None