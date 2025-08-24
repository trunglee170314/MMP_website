from typing import List, Optional
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models
from ..iam import models as user_models
from .schemas import BoardOut

class BoardRepository(Protocol):
    def list_by_user(self, user_id: int) -> List[models.Board]: ...
    def list_all_user(self) -> List[models.Board]: ...
    def get(self, board_id: int) -> Optional[models.Board]: ...
    def create_with_id(self, board_id: int, user_id: int, name: str, description: str) -> models.Board: ...
    def update(self, board: models.Board, *, name: Optional[str], description: Optional[str]) -> models.Board: ...
    def delete(self, board: models.Board) -> None: ...

class SqlAlchemyBoardRepository:
    def __init__(self, db: Session):
        self.db = db

def list_by_user(self, user_id: int) -> List[models.Board]:
    stmt = select(models.Board).where(models.Board.user_id == user_id)
    return list(self.db.execute(stmt).scalars().all())

def list_all_user(self) -> List[models.Board]:
    stmt = (select(models.Board, user_models.User).join(user_models.User, models.Board.owner_id == user_models.User.id))
    rows = self.db.execute(stmt).all()

    out: List[BoardOut] = []
    for board, user in rows:
        out.append(
            BoardOut(
                id=board.id,
                name=board.board_name,
                barcode=board.barcode,
                ip=board.ip,
                owner=user.user_name,
                note=board.note or "",
                status=board.status,
                location=board.location or "",
            )
        )
    return out

def get(self, board_id: int) -> Optional[models.Board]:
    return self.db.get(models.Board, board_id)

def create_with_id(self, board_id: int, user_id: int, name: str, description: str) -> models.Board:
    b = models.Board(id=board_id, user_id=user_id, name=name, description=description or "")
    self.db.add(b)
    self.db.commit()
    self.db.refresh(b)
    return b

def update(self, board: models.Board, *, name: Optional[str], description: Optional[str]) -> models.Board:
    if name is not None:
        board.name = name
    if description is not None:
        board.description = description
    self.db.commit(); self.db.refresh(board)
    return board

def delete(self, board: models.Board) -> None:
    self.db.delete(board)
    self.db.commit()