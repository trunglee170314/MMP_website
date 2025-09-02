from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..type_tasks.schemas import TypeTaskCreateUpdate, TypeTaskOut
from ..core.db import get_db
from ..iam.deps import require_user, require_admin
from .repository import SqlAlchemyTypeTaskRepository
from .service import TypeTaskService
from typing import List

router = APIRouter(prefix="/type_tasks", tags=["type_tasks"])

def get_user_service(db: Session = Depends(get_db)) -> TypeTaskService:
    return TypeTaskService(SqlAlchemyTypeTaskRepository(db))

# Get list of type tasks
@router.get("/", status_code=status.HTTP_200_OK, response_model= List[TypeTaskOut], dependencies=[Depends(require_user)])
def get_type_tasks(svc: TypeTaskService = Depends(get_user_service)):
    return svc.get_list_type_task()

# Create new type task
@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_type_task(payload: TypeTaskCreateUpdate, svc: TypeTaskService = Depends(get_user_service)):
    type_task = svc.create_type_task(payload)
    if not type_task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Type task creation failed")
    return {"id": type_task.id}

# Update type task
@router.patch("/{type_task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def update_type_task(type_task_id: int, payload: TypeTaskCreateUpdate, svc: TypeTaskService = Depends(get_user_service)):
    type_task = svc.update_type_task(type_task_id, payload)
    if not type_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type task not found")
    return {"id": type_task.id}

# Delete type task
@router.delete("/{type_task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def delete_type_task(type_task_id: int, svc: TypeTaskService = Depends(get_user_service)):
    type_task = svc.delete_type_task(type_task_id)
    if not type_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type task not found")
    return {"message": f"Deleted type task with ID {type_task_id} successfully."}
