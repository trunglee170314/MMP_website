from typing import Optional
from pydantic import BaseModel, ConfigDict

class BoardCreate(BaseModel):
    name: str
    description: Optional[str] = ""

class BoardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class BoardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    barcode: str
    ip: int
    owner: str
    note: Optional[str] = ""
    status: str
    location: str