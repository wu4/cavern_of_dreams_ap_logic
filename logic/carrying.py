from typing import override
from .logic import Logic, Not
from .has import CarryingItem

class Carrying(Logic):
  def __init__(self, carryable: CarryingItem | None):
    self.carryable: CarryingItem | None = carryable
    super().__init__()

  @override
  def __str__(self) -> str:
    return f"Carrying {self.carryable}"

  @override
  def into_server_code(self) -> str:
    if self.carryable is None:
      return "s._cavernofdreams_carrying[p] is None"
    else:
      return f"s._cavernofdreams_carrying[p]=={self.carryable.__repr__()}"


jester_boots = Carrying("Jester Boots")
apple = Carrying("Apple")
medicine = Carrying("Medicine")
bubble_conch = Carrying("Bubble Conch")

sages_gloves = Carrying("Sage's Gloves")
lady_opals_head = Carrying("Lady Opal's Head")
shelnerts_fish = Carrying("Shelnert's Fish")
mr_kerringtons_wings = Carrying("Mr. Kerrington's Wings")

no_temp_items = Carrying(None)

no_jester_boots = Not(jester_boots)
