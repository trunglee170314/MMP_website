from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..iam.deps import require_admin, require_user
from .repository import SqlAlchemyTaskRepository
from .service import TaskService
from .schemas import task_create, task_update, task_claim, task_out
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_user_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(SqlAlchemyTaskRepository(db))

# Admin
# Get list of tasks approval
@router.get("/admin/appr_list", status_code=status.HTTP_200_OK, response_model=List[task_out], dependencies=[Depends(require_admin)])
def appr_list(svc: TaskService = Depends(get_user_service)):
    try:
        return svc.get_list_task_waiting_appr()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete task
@router.delete("/admin/delete/{task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def delete_task(task_id: int, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.delete_task(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return {"message": f"Deleted task with ID {task_id} successfully."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Resolved task
@router.post("/admin/resolved/{task_id}", status_code=status.HTTP_200_OK, response_model=task_out, dependencies=[Depends(require_admin)])
def resolved_task(task_id: int, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.resolved_task(task_id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# approve task
@router.post("/admin/approve/{task_id}", status_code=status.HTTP_200_OK, response_model=task_out, dependencies=[Depends(require_user)])
def approve_task(task_id: int, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.approve_task(task_id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#User
# Get list task
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[task_out], dependencies=[Depends(require_user)])
def list_task(svc: TaskService = Depends(get_user_service)):
    return svc.get_list_task()

# Get detail task
@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=task_out, dependencies=[Depends(require_user)])
def detail_task(task_id: int, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.get_task_id(task_id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Create task
@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=task_out, dependencies=[Depends(require_user)])
def create_task(task_create: task_create, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.create_task(task_create)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Update task
@router.patch("/update/{task_id}", status_code=status.HTTP_200_OK, response_model=task_out, dependencies=[Depends(require_user)])
def update_task(task_id: int, task_update: task_update, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.update_task(task_id, task_update)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Claim task
@router.patch("/claim/{task_id}", status_code=status.HTTP_200_OK, response_model=task_out, dependencies=[Depends(require_user)])
def claim_task(task_id: int, task_claim: task_claim, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.task_claim(task_id, task_claim)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# complete task
@router.post("/complete/{task_id}", status_code=status.HTTP_200_OK, response_model=task_out, dependencies=[Depends(require_user)])
def complete_task(task_id: int, svc: TaskService = Depends(get_user_service)):
    try:
        task = svc.update_complete_task(task_id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)