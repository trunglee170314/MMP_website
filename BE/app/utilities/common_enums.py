from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"

class TypeTaskEnum(str, Enum):
    GST = "GST"
    OMX = "OMX"

class TaskStatusEnum(str, Enum):
    ON_GOING = "on_going"
    DONE = "done"
    NOT_YET = "not_yet"
    ON_REVIEWING = "on_reviewing"
    SUSPEND = "suspend"
    RESOLVED = "resolved"
    FREE = "free"

class TaskPriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
