from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..iam.deps import require_user
from .repository import SqlAlchemyboardRepository
from .service import boardService
from .schemas import boardCreate, boardUpdate, boardOut

router = APIRouter(prefix="/boards", tags=["boards"])