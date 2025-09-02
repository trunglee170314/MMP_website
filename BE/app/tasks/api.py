from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..iam.deps import require_admin, require_user
from .repository import SqlAlchemyTaskRepository
from .service import TaskService
from .schemas import task_create, task_update, task_claim, task_out, HttpResponse
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_user_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(SqlAlchemyTaskRepository(db))

# Get list task
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[task_out], dependencies=[Depends(require_user)])
def list_task(svc: TaskService = Depends(get_user_service)):
    tasks = svc.get_list_task()
    return [task_out.model_validate(task).model_dump(by_alias=True) for task in tasks]

# Get list of tasks approval
@router.get("/appr_list", status_code=status.HTTP_200_OK, response_model=List[task_out], dependencies=[Depends(require_user)])
def appr_list(svc: TaskService = Depends(get_user_service)):
    return svc.get_list_task_appr()

# Get detail task
@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=task_out, dependencies=[Depends(require_user)])
def detail_task(task_id: int, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.get_task_id(task_id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Create task
@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_user)])
def create_task(task_create: task_create, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.create_task(task_create)
        return {"id": task.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# approve task
@router.post("/approve/{task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_user)])
def approve_task(task_id: int, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.approve_task(task_id)
        return {"id": task.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Update task
@router.patch("/update/{task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_user)])
def update_task(task_id: int, task_update: task_update, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.update_task(task_id, task_update)
        return {"id": task.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Claim task
@router.patch("/claim/{task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_user)])
def claim_task(task_id: int, task_claim: task_claim, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.task_claim(task_id, task_claim)
        return {"id": task.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# complete task
@router.post("/complete/{task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_user)])
def complete_task(task_id: int, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.update_complete_task(task_id)
        return {"id": task.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Delete type task
@router.delete("/delete/{task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def delete_task(task_id: int, svc: TaskService = Depends(get_user_service)):
    task = svc.delete_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": f"Deleted task with ID {task_id} successfully."}