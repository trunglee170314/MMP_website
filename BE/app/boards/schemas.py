from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from ..iam.schemas import OutUser

class InBoard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    board_name: str
    barcode: int
    ip: Optional[int] = None
    owner_ids: Optional[List[int]] = None
    note: Optional[str] = None
    status: str
    location: Optional[str] = None

class OutBoard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    board_name: str
    barcode: int
    ip: Optional[int] = None
    owners: List[OutUser]
    note: Optional[str] = None
    status: str
    location: Optional[str] = None