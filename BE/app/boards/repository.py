from typing import List, Optional
from typing_extensions import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models
from ..iam import models as user_models
from .schemas import OutBoard, InBoard

class BoardRepository(Protocol):
    # def list_by_user(self, user_id: int) -> List[models.Board]: ...
    def get_by_barcode(self) -> Optional[models.Board]: ...
    def list_all_board(self) -> List[models.Board]: ...
    def get_by_id(self, board_id: int) -> Optional[models.Board]: ...
    def add_board(self, board_id: int, user_id: int, name: str, description: str) -> models.Board: ...
    def update(self, board: models.Board, payload: InBoard) -> models.Board: ...
    def delete(self, board: models.Board) -> None: ...

class SqlAlchemyBoardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_barcode(self, barcode: str) -> Optional[models.Board]:
        stmt = select(models.Board).where(models.Board.barcode == barcode)
        return self.db.execute(stmt).scalars().first()

    # def list_by_user(self, user_id: int) -> List[models.Board]:
    #     stmt = select(models.Board).where(models.Board.user_id == user_id)
    #     return list(self.db.execute(stmt).scalars().all())

    def list_all_board(self) -> List[models.Board]:
        return self.db.scalars(select(models.Board)).all()

    def get_by_id(self, board_id: int) -> Optional[models.Board]:
        b = self.db.get(models.Board, board_id)
        if not b:
            return None
        return b

    def add_board(self, payload: InBoard) -> models.Board:
        b = models.Board(
            board_name = payload.board_name,
            barcode = payload.barcode,
            ip = payload.ip,
            owner = payload.owner,
            note = payload.note,
            status = payload.status,
            location = payload.location)
        self.db.add(b)
        self.db.commit()
        self.db.refresh(b)
        return b

    def update(self, board: models.Board, payload: InBoard) -> models.Board:
        data = payload.dict(exclude_unset=True)
        for field, value in data.items():
            setattr(board, field, value)
        self.db.commit(); self.db.refresh(board)
        return board

    def delete(self, board: models.Board) -> None:
        self.db.delete(board)
        self.db.commit()