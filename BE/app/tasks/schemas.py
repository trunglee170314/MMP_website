from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from ..utilities.common_enums import TypeTaskEnum, TaskPriorityEnum, TaskStatusEnum
from ..boards.schemas import OutBoard
from ..classifications.schemas import ClassificationOut
from ..iam.schemas import OutUser

class task_out(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    type_task : TypeTaskEnum
    description : Optional[str] = None
    pic: Optional[OutUser] = None
    classification : Optional[ClassificationOut] = None
    start_date : Optional[datetime] = None
    due_date : Optional[datetime] = None
    redmine : Optional[str] = None
    board : Optional[OutBoard] = None
    note : Optional[str] = None
    score : Optional[int] = None
    status : TaskStatusEnum
    priority: Optional[TaskPriorityEnum] = None
    approve_status : bool

class task_update(BaseModel):
    type: TypeTaskEnum
    board_id: int
    pic_id: int
    description: Optional[str] = None
    priority: TaskPriorityEnum
    classication_id: int
    start_date : Optional[datetime] = None
    due_date : Optional[datetime] = None
    redmine: Optional[str] = None
    note: Optional[str] = None
    score: Optional[int] = None
    status : TaskStatusEnum

class task_create(BaseModel) :
    type : TypeTaskEnum
    board_id : int
    description : Optional[str] = None
    pic_id : int
    classication_id : int
    start_date : Optional[datetime] = None
    due_date : Optional[datetime] = None
    redmine : Optional[str] = None
    note : Optional[str] = None
    score : Optional[int] = None
    priority: TaskPriorityEnum

class task_claim(BaseModel):
    pic: int