from . import Logic

from typing import TypeAlias, Literal

DifficultyType: TypeAlias = Literal["Intermediate", "Hard"]

class Difficulty(Logic):
  def __str__(self) -> str:
    return f"Difficulty: {self.difficulty}"
  
  def __init__(self, difficulty: DifficultyType) -> None:
    self.difficulty = difficulty
    super().__init__()
    
Intermediate = Difficulty("Intermediate")
Hard = Difficulty("Hard")