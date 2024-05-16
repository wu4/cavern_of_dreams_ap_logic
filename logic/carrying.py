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
apple = Carrying("Apple")
potion = Carrying("Potion")
bubble_conch = Carrying("Bubble Conch")

no_throwables = _NoThrowables()

no_jester_boots = _NoJesterBoots()

plant_and_climb_tree = _PlantAndClimbTree()

no_temp_items = no_throwables & no_jester_boots
