from typing import TypeAlias

from . import Logic
from . import carrying
from ..generated import abilityItem, nonVanillaAbilityItem, pickupItem

HasItemType: TypeAlias = abilityItem | nonVanillaAbilityItem | pickupItem

class Collected(Logic):
  def __str__(self) -> str:
    return f"Has {self.item}"
  
  def __init__(self, item: HasItemType) -> None:
    self.item = item
    super().__init__()

Wings: Logic = Collected("Wings")
DoubleJump: Logic = Collected("Double Jump")
Bubble: Logic = Collected("Bubble")
Flight: Logic = Collected("Flight")
Roll: Logic = Collected("Roll")
Sprint: Logic = Collected("Sprint")
HighJump: Logic = Collected("High Jump")
Swim: Logic = Collected("Swim")
Carry: Logic = Collected("Carry")
SuperBounce: Logic = Collected("Super Bounce")
SuperBubbleJump: Logic = Collected("Super Bubble Jump")
AirSwim: Logic = Collected("Air Swim")

FishFood: Logic = Collected("Fish Food")

Horn: Logic = carrying.NoThrowables & Collected("Horn")
AirTail: Logic = carrying.NoThrowables & Collected("Aerial Tail")
GroundTail: Logic = carrying.NoThrowables & Collected("Grounded Tail")
Climb: Logic = carrying.NoThrowables & Collected("Climb")