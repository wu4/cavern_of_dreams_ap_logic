from typing import TypeAlias, Literal
from . import Logic
from . import item

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
  
class _ClimbPlantedTree(Logic):
  def __str__(self) -> str:
    return "Climb planted tree"

JesterBoots = Carrying("Jester Boots")
Apple = Carrying("Apple") & item.Carry
Potion = Carrying("Potion") & item.Carry
BubbleConch = Carrying("Bubble Conch") & item.Carry

NoThrowables = _NoThrowables()
NoJesterBoots = _NoJesterBoots()

Nothing = NoThrowables & NoJesterBoots