from . import Logic

from typing import TypeAlias, Literal, override

DifficultyType: TypeAlias = Literal["Intermediate", "Hard"]

class Difficulty(Logic):
  @override
  def __str__(self) -> str:
    return f"Difficulty: {self.difficulty}"
  
  def __init__(self, difficulty: DifficultyType) -> None:
    super().__init__()
    self.difficulty = difficulty
    
Intermediate = Difficulty("Intermediate")
Hard = Difficulty("Hard")
