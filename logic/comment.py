from typing import override
from .logic import Logic

class Comment(Logic):
  comment: str
  logic: Logic

  @override
  def __str__(self) -> str:
    return f"'{self.comment}' ({self.logic})"

  @override
  def into_server_code(self) -> str:
    return self.logic.into_server_code()

  def __init__(self, comment: str, logic: Logic) -> None:
    super().__init__()
    self.comment = comment
    self.logic = logic
