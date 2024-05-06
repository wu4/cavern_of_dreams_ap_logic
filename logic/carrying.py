from typing import TypeAlias, Literal
from . import Logic

CarryingType: TypeAlias = Literal[
  "Jester Boots",
  "Apple",
  "Potion",
  "Bubble Conch"
]

class Carrying(Logic):
  def __str__(self) -> str:
    return f"Carrying {self.carrying}"
  
  def __init__(self, carrying: CarryingType) -> None:
    self.carrying = carrying
    super().__init__()

class _NoThrowables(Logic):
  def __str__(self) -> str:
    return "Not carrying any throwables"

class _NoJesterBoots(Logic):
  def __str__(self) -> str:
    return "Not carrying Jester Boots"
  
class _PlantAndClimbTree(Logic):
  def __str__(self) -> str:
    return "Climb planted tree"

JesterBoots = Carrying("Jester Boots")
Apple = Carrying("Apple")
Potion = Carrying("Potion")
BubbleConch = Carrying("Bubble Conch")

NoThrowables = _NoThrowables()

NoJesterBoots = _NoJesterBoots()

PlantAndClimbTree = _PlantAndClimbTree()

NoTempItems = NoThrowables & NoJesterBoots