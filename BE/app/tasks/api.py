from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..iam.deps import require_user
from .repository import SqlAlchemyTaskRepository
from .service import TaskService
from .schemas import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(SqlAlchemyTaskRepository(db))


@router.get("/", response_model=list[TaskOut])
def list_my_tasks(current=Depends(require_user), svc: TaskService = Depends(get_service)):
    return svc.repo.list_by_user(current.id)


@router.post("/", response_model=TaskOut)
def create_task(payload: TaskCreate, current=Depends(require_user), svc: TaskService = Depends(get_service)):
    return svc.create_task(current.id, payload.title)


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, current=Depends(require_user), svc: TaskService = Depends(get_service)):
    try:
        return svc.update_task(current.id, task_id, title=payload.title, done=payload.done)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}")
def delete_task(task_id: int, current=Depends(require_user), svc: TaskService = Depends(get_service)):
    try:
        svc.delete_task(current.id, task_id)
        return {"message": "Task deleted"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")