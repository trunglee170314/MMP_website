from typing import Optional
from pydantic import BaseModel, ConfigDict

class InBoard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    board_name: str
    barcode: int
    ip: Optional[int] = None
    owner: Optional[str] = None
    note: Optional[str] = None
    status: str
    location: Optional[str] = None

class OutBoard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    board_name: str
    barcode: int
    ip: Optional[int] = None
    owner: Optional[str] = None
    note: Optional[str] = None
    status: str
    location: Optional[str] = None