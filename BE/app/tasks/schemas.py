from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from ..boards.schemas import OutBoard
from ..type_tasks.schemas import TypeTaskOut
from ..iam.schemas import OutUser

class HttpResponse(BaseModel):
    status: int
    message: str
    data: Optional[Any] = None

class task_out(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id : int
    type_task : Optional[TypeTaskOut]
    description : str
    pic: Optional[OutUser]
    classify : str
    start_date : datetime
    due_date : Optional[datetime] = None
    redmine : str
    board : Optional[OutBoard]
    note : str
    score : int
    status : str
    priority: str
    approve_status : bool

class task_update(BaseModel):
    type_task_id: int
    board_id: int
    pic: int
    description: str
    priority: str
    classify: str
    redmine: str
    note: Optional[str] = None
    score: Optional[int] = None

class task_create(BaseModel) :
    type_task_id : int
    board_id : int
    description : str
    pic_id : int
    classify : str
    start_date : datetime
    due_date : Optional[datetime] = None
    redmine : str
    note : str
    score : int
    status : str
    priority: str

class task_claim(BaseModel):
    pic: int
    status: str