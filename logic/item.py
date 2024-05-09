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
Flight: Logic = Collected("Flight")
roll: Logic = Collected("Roll")
sprint: Logic = Collected("Sprint")
high_jump: Logic = Collected("High Jump")
swim: Logic = Collected("Swim")
Carry: Logic = Collected("Carry")
SuperBounce: Logic = Collected("Super Bounce")
SuperBubbleJump: Logic = Collected("Super Bubble Jump")
AirSwim: Logic = Collected("Air Swim")

FishFood: Logic = Collected("Fish Food")

horn: Logic = carrying.NoThrowables & Collected("Horn")
air_tail: Logic = carrying.NoThrowables & Collected("Aerial Tail")
ground_tail: Logic = carrying.NoThrowables & Collected("Grounded Tail")
Climb: Logic = carrying.NoThrowables & Collected("Climb")
