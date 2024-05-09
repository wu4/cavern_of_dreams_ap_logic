from typing import override
from . import Logic

class Comment(Logic):
  comment: str
  logic: Logic

  @override
  def __str__(self) -> str:
    return f"'{self.comment}' ({self.logic})"

  def __init__(self, comment: str, logic: Logic) -> None:
    super().__init__()
    self.comment = comment
    self.logic = logic
