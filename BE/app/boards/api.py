from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.db import get_db
from ..iam.deps import require_user
from ..iam.repository import SqlAlchemyUserRepository
from .repository import SqlAlchemyBoardRepository
from .service import BoardService
from .schemas import InBoard, OutBoard

router = APIRouter(prefix="/boards", tags=["boards"])

def get_board_service(db: Session = Depends(get_db)) -> BoardService:
    return BoardService(SqlAlchemyBoardRepository(db), SqlAlchemyUserRepository(db))

# Get all boards
@router.get("/", response_model=List[OutBoard], dependencies = [Depends(require_user)])
def list_all_board(svc: BoardService = Depends(get_board_service)):
    return svc.list_all_board()

# Get my boards
@router.get("/me", response_model=List[OutBoard], dependencies = [Depends(require_user)])
def list_my_board(current_user = Depends(require_user),
                  svc: BoardService = Depends(get_board_service)):
        return svc.list_my_boards(current_user.id)

# Get a board
@router.get("/{board_id}", response_model=OutBoard, dependencies = [Depends(require_user)])
def get_board_by_id(board_id: int, svc: BoardService = Depends(get_board_service)):
    try:
        return svc.get_by_id(board_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Add a board
@router.post("/add",
             response_model=OutBoard,
             status_code=status.HTTP_201_CREATED,
             dependencies = [Depends(require_user)])
def add_a_board(payload: InBoard,
                svc: BoardService = Depends(get_board_service)):
    try:
        return svc.add_board(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Delete a board
@router.delete("/delete/{board_id}", status_code=status.HTTP_200_OK, dependencies = [Depends(require_user)])
def delete_board(board_id: int, svc: BoardService = Depends(get_board_service)):
    try:
        svc.delete_board(board_id)
        return {"message": "Board %d deleted" % (board_id)}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Update a board
@router.put("/update/{board_id}",
            response_model=OutBoard,
            status_code=status.HTTP_200_OK,
            dependencies = [Depends(require_user)])
def update_board(board_id: int, payload: InBoard, svc: BoardService = Depends(get_board_service)):
    try:
        return svc.update_board(board_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)