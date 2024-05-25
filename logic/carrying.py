from typing import override
from . import Logic

class Carrying(Logic):
  @override
  def __str__(self) -> str:
    return f"Carrying {self.carrying}"

  def __init__(self, carrying: str) -> None:
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
medicine = Carrying("Medicine")
bubble_conch = Carrying("Bubble Conch")

sages_gloves = Carrying("Sage's Gloves")
lady_opals_head = Carrying("Lady Opal's Head")
shelnerts_fish = Carrying("Shelnert's Fish")
mr_kerringtons_wings = Carrying("Mr. Kerrington's Wings")

no_throwables = _NoThrowables()

no_jester_boots = _NoJesterBoots()

plant_and_climb_tree = _PlantAndClimbTree()

no_temp_items = no_throwables & no_jester_boots
