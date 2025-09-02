from typing import List, Optional
from typing_extensions import Protocol
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from . import models
from ..iam import models as user_models
from ..iam.association import user_board
from .schemas import OutBoard, InBoard

class BoardRepository(Protocol):
    def list_by_user(self, user_id: int) -> List[models.Board]: ...
    def get_by_barcode(self) -> Optional[models.Board]: ...
    def list_all_board(self) -> List[models.Board]: ...
    def get_by_id(self, board_id: int) -> Optional[models.Board]: ...
    def add(self, payload: InBoard, owners: List[user_models.User]) -> models.Board: ...
    def update(self, board: models.Board, payload: InBoard, owners: List[user_models.User]) -> models.Board: ...
    def delete(self, board: models.Board) -> None: ...

class SqlAlchemyBoardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_barcode(self, barcode: str) -> Optional[models.Board]:
        stmt = select(models.Board).where(models.Board.barcode == barcode)
        return self.db.execute(stmt).scalars().first()

    def list_by_user(self, user_id: int) -> List[models.Board]:
        stmt = (select(models.Board)
        .join(models.user_board, models.Board.id == models.user_board.c.board_id)
        .where(models.user_board.c.user_id == user_id)
        .options(selectinload(models.Board.owners))
        )
        return self.db.scalars(stmt).all()

    def list_all_board(self) -> List[models.Board]:
        return self.db.scalars(
            select(models.Board).options(selectinload(models.Board.owners))
            ).all()

    def get_by_id(self, board_id: int) -> Optional[models.Board]:
        b = self.db.get(models.Board, board_id)
        return b

    def add(self, payload: InBoard, owners: List[user_models.User]) -> models.Board:
        b = models.Board(
            board_name = payload.board_name,
            barcode = payload.barcode,
            ip = payload.ip,
            note = payload.note or "",
            status = payload.status,
            location = payload.location or "",
            owners = list(owners)
            )

        self.db.add(b)
        self.db.commit()
        self.db.refresh(b)
        return b

    def update(self, board: models.Board, payload: InBoard, owners: List[user_models.User]) -> models.Board:
        data = payload.dict(exclude_unset=True)
        for field, value in data.items():
            setattr(board, field, value)

        board.owners = list(owners)

        self.db.commit(); self.db.refresh(board)
        return board

    def delete(self, board: models.Board) -> None:
        self.db.delete(board)
        self.db.commit()