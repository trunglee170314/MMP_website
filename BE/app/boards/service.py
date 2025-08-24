from typing import Optional
from .repository import BoardRepository
from . import models

class BoardService:
    def __init__(self, repo: BoardRepository):
        self.repo = repo

    def list_all_board(self):
        return self.repo.list_all_user()

    def list_my_boards(self, user_id: int):
        return self.repo.list_by_user(user_id)

    def get_my_board(self, user_id: int, board_id: int) -> models.Board:
        b = self.repo.get(board_id)
        if not b or b.user_id != user_id:
            raise ValueError("Board not found")
        return b

    def create_board_with_id(self, user_id: int, board_id: int, name: str, description: str) -> models.Board:
        if self.repo.get(board_id):
            raise ValueError("Board id already exists")
        return self.repo.create_with_id(board_id, user_id, name, description)

    def update_board(self, user_id: int, board_id: int, *, name: Optional[str], description: Optional[str]) -> models.Board:
        b = self.get_my_board(user_id, board_id)
        return self.repo.update(b, name=name, description=description)

    def delete_board(self, user_id: int, board_id: int) -> None:
        b = self.get_my_board(user_id, board_id)
        self.repo.delete(b)