from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint
from ..core.db import Base

user_board = Table(
    "user_board",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("board_id", ForeignKey("boards.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("user_id", "board_id", name="uq_user_board"),
)