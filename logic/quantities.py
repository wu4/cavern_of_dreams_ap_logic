from typing import override
from . import Logic

class HasEggs(Logic):
  @override
  def __str__(self) -> str:
    return f"Has at least {self.eggs} eggs"

  def __init__(self, eggs: int) -> None:
    self.eggs = eggs
    super().__init__()

class HasHearts(Logic):
  @override
  def __str__(self) -> str:
    return f"Has at least {self.hearts} hearts"

  def __init__(self, hearts: int) -> None:
    self.hearts = hearts
    super().__init__()

class HasShrooms(Logic):
  @override
  def __str__(self) -> str:
    return f"Has enough shrooms for the {self.shroom_count_source} fella"

  def __init__(self, shroom_count_source: str):
    super().__init__()
    self.shroom_count_source = shroom_count_source
