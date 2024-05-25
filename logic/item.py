from typing import TypeAlias, override

from . import Logic
from . import carrying
from ..generated import abilityItem, nonVanillaAbilityItem, pickupItem

HasItemType: TypeAlias = abilityItem | nonVanillaAbilityItem | pickupItem

class Collected(Logic):
  @override
  def __str__(self) -> str:
    return f"Has {self.item}"

  def __init__(self, item: HasItemType) -> None:
    self.item = item
    super().__init__()

wings: Logic = Collected("Wings")
double_jump: Logic = Collected("Double Jump")
bubble: Logic = Collected("Bubble")
flight: Logic = Collected("Flight")
roll: Logic = Collected("Roll")
sprint: Logic = Collected("Sprint")
high_jump: Logic = Collected("High Jump")
swim: Logic = Collected("Swim")
carry: Logic = Collected("Carry")
super_bounce: Logic = Collected("Super Bounce")
super_bubble_jump: Logic = Collected("Super Bubble Jump")
air_swim: Logic = Collected("Air Swim")

fish_food: Logic = Collected("Fish Food")

horn: Logic = carrying.no_throwables & Collected("Horn")
air_tail: Logic = carrying.no_throwables & Collected("Aerial Tail")
ground_tail: Logic = carrying.no_throwables & Collected("Grounded Tail")
climb: Logic = carrying.no_throwables & Collected("Climb")
