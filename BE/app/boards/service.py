from typing import Optional, List
from fastapi import HTTPException

from . import models
from ..iam import models as user_models
from ..iam.repository import UserRepository
from .repository import BoardRepository
from .schemas import InBoard

class BoardService:
    def __init__(self, repo: BoardRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo

    # helpers
    def _found_board(self, b: models.Board) -> models.Board:
        if not b:
            raise ValueError("Board not found")
        return b

    def _found_user(self, u: user_models.User) -> user_models.User:
        if not u:
            raise ValueError("User not found")
        return u

    # actions
    def list_all_board(self) -> List[models.Board]:
        return self.repo.list_all_board()

    def list_my_boards(self, user_id: int):
        return self.repo.list_by_user(user_id)

    def get_by_id(self, board_id: int) -> models.Board:
        return self._found_board(self.repo.get_by_id(board_id))

    def add_board(self, payload: InBoard) -> models.Board:
        if self.repo.get_by_barcode(payload.barcode):
            raise ValueError("Board already existed")
        owners = self.user_repo.get_by_ids(payload.owner_ids)
        if len(owners) != len(set(payload.owner_ids)):
            raise ValueError("Some owner_ids not found")

        return self.repo.add(payload, owners)

    def update_board(self, board_id: int, payload: InBoard) -> models.Board:
        board = self._found_board(self.repo.get_by_id(board_id))

        if payload.barcode and payload.barcode != board.barcode:
            if self.repo.get_by_barcode(payload.barcode):
                raise ValueError("Barcode already exists")

        owners = self.user_repo.get_by_ids(payload.owner_ids)
        if len(owners) != len(set(payload.owner_ids)):
            raise ValueError("Some owner_ids not found")

        return self.repo.update(self.get_by_id(board_id), payload, owners)

    def delete_board(self, board_id: int) -> None:
        b = self.get_by_id(board_id)
        self.repo.delete(b)