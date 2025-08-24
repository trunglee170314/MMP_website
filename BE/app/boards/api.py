from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..iam.deps import require_user, require_admin
from .repository import SqlAlchemyBoardRepository
from .service import BoardService
from .schemas import BoardCreate, BoardUpdate, BoardOut

router = APIRouter(prefix="/boards", tags=["boards"])

def get_service(db: Session = Depends(get_db)) -> BoardService:
    return BoardService(SqlAlchemyBoardRepository(db))

# Get all boards
@router.get("/", response_model=list[BoardOut], dependencies = [Depends(require_admin)])
def list_all_board(svc: BoardService = Depends(get_service)):
    return svc.list_all_board()

# Get board by user (hidden)
@router.get("/user", response_model=list[BoardOut])
def list_user_boards(current=Depends(require_user), svc: BoardService = Depends(get_service)):
    return svc.list_my_boards(current.id)

# Get a board
@router.get("/{board_id}", response_model=BoardOut)
def get_board(board_id: int, current=Depends(require_user), svc: BoardService = Depends(get_service)):
    try:
        return svc.get_my_board(current.id, board_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Board not found")

# Add a board
@router.post("/{board_id}", response_model=BoardOut, status_code=201)
def add_board(board_id: int, payload: BoardCreate, current=Depends(require_user), svc: BoardService = Depends(get_service)):
    try:
        return svc.create_board_with_id(current.id, board_id, payload.name, payload.description or "")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete a board
@router.delete("/delete/{board_id}")
def delete_board(board_id: int, current=Depends(require_user), svc: BoardService = Depends(get_service)):
    try:
        svc.delete_board(current.id, board_id)
        return {"message": "Board deleted"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Board not found")

# Update a board
@router.put("/update/{board_id}", response_model=BoardOut)
def update_board(board_id: int, payload: BoardUpdate, current=Depends(require_user), svc: BoardService = Depends(get_service)):
    try:
        return svc.update_board(current.id, board_id, name=payload.name, description=payload.description)
    except ValueError:
        raise HTTPException(status_code=404, detail="Board not found")