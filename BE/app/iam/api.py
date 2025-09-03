from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core.db import get_db
from ..core.security import create_access_token
from .schemas import InUserCreate, OutUser, InUserUpdate, InLogin, OutToken
from .repository import SqlAlchemyUserRepository
from .service import UserService
from .deps import require_admin, require_user, get_current_user
from . import models

router = APIRouter(prefix="", tags=["iam"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(SqlAlchemyUserRepository(db))

# Register a new account
@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(payload: InUserCreate, svc: UserService = Depends(get_user_service)):
    try:
        user = svc.register(payload)
        return {"id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Login
@router.post("/auth/login", response_model=OutToken)
def login(payload: InLogin, svc: UserService = Depends(get_user_service)):
    try:
        user = svc.authenticate(payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    token = create_access_token(
        {
            "sub": user.email,
            "full_name": user.full_name,
            "code": user.code,
            "number_phone": user.number_phone,
            "auth_registered": user.auth_registered,
            "user_name": user.user_name,
            "role": user.role
        })

    return {
        "access_token": token["access_token"],
        "token_type": "bearer",
        "expire": token["expire"],
    }

# Get waiting approve list (admin)
@router.get("/user/admin/appr_list", response_model=List[OutUser], dependencies=[Depends(require_admin)])
def appr_list(svc: UserService = Depends(get_user_service)):
    return svc.list_waiting_approve()

# Approve a user (admin)
@router.post("/user/admin/approve/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def approve_user(user_id: int, svc: UserService = Depends(get_user_service)):
    try:
        user = svc.approve_user(user_id)
        return {"id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Update user role (admin)
@router.patch("/user/admin/update_role/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def update_role(user_id: int, role: str, svc: UserService = Depends(get_user_service)):
    user = svc.update_role(user_id, role)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"id": user.id}

# Reset password (admin)
@router.post("/user/admin/reset_pw/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def reset_password(user_id: int, svc: UserService = Depends(get_user_service)):
    try:
        reset_pwd = svc.reset_password(user_id)
        return {"id": reset_pwd.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete an account (admin)
@router.delete("/user/admin/delete/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def delete_user(user_id: int,
                svc: UserService = Depends(get_user_service),
                current_user: models.User = Depends(get_current_user)):
        if user_id == current_user.id:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin cannot delete their own account via this endpoint")
        if not svc.delete_user(user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"detail": "User deleted"}

# Update current account information
@router.put("/user/update", status_code=status.HTTP_200_OK, dependencies=[Depends(require_user)])
def update_user(payload: InUserUpdate, svc: UserService = Depends(get_user_service)):
    try:
        user = svc.update_user(payload)
        return {"id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get a user information
@router.get("/user/{user_id}", response_model=OutUser, dependencies=[Depends(require_user)])
def get_user(user_id: int , svc: UserService = Depends(get_user_service)):
    try:
        user = svc.get_user_by_id(user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Get all approved user information (admin)
@router.get("/users", response_model=List[OutUser], dependencies=[Depends(require_admin)])
def list_user(svc: UserService = Depends(get_user_service)):
    return svc.get_list_appr_user()