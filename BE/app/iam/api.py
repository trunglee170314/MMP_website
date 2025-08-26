from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..core.security import create_access_token
from .schemas import UserCreate, UserOut, UserUpdate, LoginInput, HttpResponse
from .repository import SqlAlchemyUserRepository
from .service import UserService
from .deps import require_admin, require_user
from typing import List

router = APIRouter(prefix="", tags=["iam"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(SqlAlchemyUserRepository(db))

# Auth
@router.post("/auth/register", response_model=HttpResponse)
def register(payload: UserCreate, svc: UserService = Depends(get_user_service)):
    try:
        user = svc.register(payload)
        if user is None:
            return HttpResponse(status= status.HTTP_400_BAD_REQUEST, message="Registration failed", data=None)
        return HttpResponse(status= status.HTTP_201_CREATED, message="Registration Success", data=UserOut.from_orm(user))
    except Exception as e:
        return HttpResponse(status= status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e), data=None)

@router.post("/auth/login", response_model=HttpResponse)
def login(payload: LoginInput, svc: UserService = Depends(get_user_service)):
    user = svc.authenticate(payload.email, payload.password)
    if not user:
        return HttpResponse(status= status.HTTP_401_UNAUTHORIZED, message="Invalid credentials", data=None)
    
    token = create_access_token(
        {
            "sub": user.email,
            "full_name": user.full_name,
            "code": user.code,
            "number_phone": user.number_phone,
            "auth_registered": user.auth_registered,
            "user_name": user.user_name,
            "role": user.role
        }, 15)
    
    return HttpResponse(status= status.HTTP_200_OK, message="Login success", data=token)

# Admin
@router.get("/user/admin/appr_list", response_model=HttpResponse, dependencies=[Depends(require_admin)])
def appr_list(svc: UserService = Depends(get_user_service)):
    users = svc.list_waiting_approve()
    user_list = [UserOut.from_orm(u) for u in users]
    return HttpResponse(status=status.HTTP_200_OK, message="Waiting users fetched", data=user_list)

@router.post("/user/admin/approve/{user_id}", response_model=HttpResponse, dependencies=[Depends(require_admin)])
def approve_user(user_id: int, svc: UserService = Depends(get_user_service)):
    user = svc.approve_user(user_id)
    if not user:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST, message="User not found")
    return HttpResponse(status=status.HTTP_200_OK, message="User approved successfully")

@router.patch("/user/admin/update_role/{user_id}", response_model=HttpResponse, dependencies=[Depends(require_admin)])
def update_role(user_id: int, role: str, svc: UserService = Depends(get_user_service)):
    user = svc.update_role(user_id, role)
    if not user:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST, message="User not found")
    return HttpResponse(status=status.HTTP_200_OK, message="User updated successfully")

@router.post("/user/admin/reset_pw/{user_id}", response_model=HttpResponse, dependencies=[Depends(require_admin)])
def reset_password(user_id: int, password: str, svc: UserService = Depends(get_user_service)):
    user_reset_password = svc.reset_password(user_id, password)
    if not user_reset_password:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST, message="User not found")
    return HttpResponse(status=status.HTTP_200_OK, message="Password reset successfully")

@router.delete("/user/admin/{user_id}", dependencies=[Depends(require_admin)])
def delete_user(user_id: int, svc: UserService = Depends(get_user_service)):
    try:
        deleted = svc.delete_user(user_id)
        if deleted:
            return HttpResponse(status=status.HTTP_200_OK, message="User deleted successfully", data=None)
        return HttpResponse(status=status.HTTP_404_NOT_FOUND, message="User not found", data=None)
    except Exception as e:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e), data=None)

# User
@router.put("/user/update", response_model=HttpResponse, dependencies=[Depends(require_user)])
def update_user(payload: UserUpdate, svc: UserService = Depends(get_user_service)):
    try:
        user = svc.update_user(payload)
        print(user)
        if user:
            return HttpResponse(status=status.HTTP_200_OK, message="User update successfully", data=None)
        return HttpResponse(status=status.HTTP_404_NOT_FOUND, message="User not found", data=None)
    except Exception as e:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e), data=None)

@router.get("/user/{user_id}", response_model=HttpResponse, dependencies=[Depends(require_user)])
def get_user(user_id: int , svc: UserService = Depends(get_user_service)):
    user = svc.get_user_by_id(user_id)
    return HttpResponse(status= status.HTTP_200_OK, message="Successfully retrieved user", data=UserOut.from_orm(user))

@router.get("/users", response_model=HttpResponse, dependencies=[Depends(require_user)])
def list_user(svc: UserService = Depends(get_user_service)):
    users = svc.get_list_user()
    user_list = [UserOut.from_orm(u) for u in users]
    return HttpResponse(status= status.HTTP_200_OK, message="Successfully retrieved users", data=user_list)