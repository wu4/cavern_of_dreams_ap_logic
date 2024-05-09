from typing import TypeAlias, Literal, override
from . import Logic

CarryingType: TypeAlias = Literal[
  "Jester Boots",
  "Apple",
  "Potion",
  "Bubble Conch"
]

class Carrying(Logic):
  @override
  def __str__(self) -> str:
    return f"Carrying {self.carrying}"
  
  def __init__(self, carrying: CarryingType) -> None:
    self.carrying = carrying
    super().__init__()

class _NoThrowables(Logic):
  @override
  def __str__(self) -> str:
    return "Not carrying any throwables"

class _NoJesterBoots(Logic):
  @override
  def __str__(self) -> str:
    return "Not carrying Jester Boots"
  
class _PlantAndClimbTree(Logic):
  @override
  def __str__(self) -> str:
    return "Climb planted tree"

jester_boots = Carrying("Jester Boots")
Apple = Carrying("Apple")
Potion = Carrying("Potion")
BubbleConch = Carrying("Bubble Conch")

NoThrowables = _NoThrowables()

no_jester_boots = _NoJesterBoots()

PlantAndClimbTree = _PlantAndClimbTree()

NoTempItems = NoThrowables & no_jester_boots
