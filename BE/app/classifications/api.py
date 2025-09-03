from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..classifications.schemas import ClassificationCreateUpdate, ClassificationOut
from ..core.db import get_db
from ..iam.deps import require_user, require_admin
from .repository import SqlAlchemyClassificationRepository
from .service import ClassificationService
from typing import List

router = APIRouter(prefix="/classifications", tags=["classifications"])

def get_user_service(db: Session = Depends(get_db)) -> ClassificationService:
    return ClassificationService(SqlAlchemyClassificationRepository(db))

# Get list of classification
@router.get("/", status_code=status.HTTP_200_OK, response_model= List[ClassificationOut], dependencies=[Depends(require_user)])
def get_classification(svc: ClassificationService = Depends(get_user_service)):
    try:
        return svc.get_list_classification()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get detail of classification
@router.get("/{classification_id}", status_code=status.HTTP_200_OK, response_model= ClassificationOut, dependencies=[Depends(require_user)])
def get_classification(classification_id: int, svc: ClassificationService = Depends(get_user_service)):
    try:
        return svc.get_classification_by_id(classification_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create new classification
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= ClassificationOut, dependencies=[Depends(require_admin)])
def create_classification(payload: ClassificationCreateUpdate, svc: ClassificationService = Depends(get_user_service)):
    try:
        classication = svc.create_classification(payload)
        return classication
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Update classification
@router.patch("/{classification_id}", status_code=status.HTTP_200_OK, response_model= ClassificationOut, dependencies=[Depends(require_admin)])
def update_classification(classification_id: int, payload: ClassificationCreateUpdate, svc: ClassificationService = Depends(get_user_service)):
    try:
        classication = svc.update_classification(classification_id, payload)
        return classication
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete classification
@router.delete("/{classification_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def delete_classifycation(classification_id: int, svc: ClassificationService = Depends(get_user_service)):
    try:
        svc.delete_classification(classification_id)
        return {"message": f"Successfully deleted classification with ID {classification_id}."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)