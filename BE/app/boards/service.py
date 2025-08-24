from typing import Optional

from . import models
from .repository import BoardRepository
from .schemas import InBoard

class BoardService:
    def __init__(self, repo: BoardRepository):
        self.repo = repo

    # helpers
    def _board_found(self, b: models.Board) -> models.Board:
        if not b:
            raise ValueError("Board not found")
        return b

    # actions
    def list_all_board(self):
        return self.repo.list_all_board()

    # def list_my_boards(self, user_id: int):
    #     return self.repo.list_by_user(user_id)

    def get_by_id(self, board_id: int) -> models.Board:
        return self._board_found(self.repo.get_by_id(board_id))

    def add_board(self, payload: InBoard) -> models.Board:
        if self.repo.get_by_barcode(payload.barcode):
            raise ValueError("Board already existed")
        return self.repo.add_board(payload)

    def update_board(self, board_id: int, payload: InBoard) -> models.Board:
        return self.repo.update(self.get_by_id(board_id), payload)

    def delete_board(self, board_id: int) -> None:
        b = self.get_by_id(board_id)
        self.repo.delete(b)