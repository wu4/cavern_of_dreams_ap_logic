from typing import override
from .logic import Logic, Not, Any
from .has import CarryingItem

class Carrying(Logic):
  def __init__(self, carryable: CarryingItem | None):
    self.carryable = carryable
    super().__init__()

  @override
  def __str__(self) -> str:
    return f"Carrying {self.carryable}"

  @override
  def into_server_code(self) -> str:
    if self.carryable is None:
      return f"s._cavernofdreams_carrying_throwable[p] is None"
    else:
      return f"s._cavernofdreams_carrying_throwable[p] == {self.carryable.__repr__()}"

class WearingJesterBoots(Logic):
  def __init__(self):
    super().__init__()

  @override
  def __str__(self) -> str:
    return "Wearing Jester Boots"

  @override
  def into_server_code(self) -> str:
    return f"s._cavernofdreams_wearing_jester_boots[p]"

class _PlantAndClimbTree(Logic):
  @override
  def __str__(self) -> str:
    return "Climb planted tree"

  @override
  def into_server_code(self) -> str:
    return "s.try_plant_and_climb_tree()"

jester_boots = WearingJesterBoots()
apple = Carrying("Apple")
medicine = Carrying("Medicine")
bubble_conch = Carrying("Bubble Conch")

sages_gloves = Carrying("Sage's Gloves")
lady_opals_head = Carrying("Lady Opal's Head")
shelnerts_fish = Carrying("Shelnert's Fish")
mr_kerringtons_wings = Carrying("Mr. Kerrington's Wings")

no_throwables = Carrying(None)

no_jester_boots = Not(jester_boots)

plant_and_climb_tree = _PlantAndClimbTree()

no_temp_items = no_throwables & no_jester_boots
