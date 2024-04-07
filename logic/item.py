from __future__ import annotations
from typing import TypeAlias

from . import Logic
from ..generated import abilityItem, nonVanillaAbilityItem, pickupItem

HasItemType: TypeAlias = abilityItem | nonVanillaAbilityItem | pickupItem

class HasItem(Logic):
  def __str__(self) -> str:
    return f"Has {self.has}"
  
  def __init__(self, has: HasItemType) -> None:
    self.has = has
    super().__init__()

Wings: Logic = HasItem("Wings")
DoubleJump: Logic = HasItem("Double Jump")
Bubble: Logic = HasItem("Bubble")
Flight: Logic = HasItem("Flight")
Roll: Logic = HasItem("Roll")
Sprint: Logic = HasItem("Sprint")
HighJump: Logic = HasItem("High Jump")
Swim: Logic = HasItem("Swim")
Carry: Logic = HasItem("Carry")
SuperBounce: Logic = HasItem("Super Bounce")
SuperBubbleJump: Logic = HasItem("Super Bubble Jump")
AirSwim: Logic = HasItem("Air Swim")

from . import carrying

Horn: Logic = carrying.NoThrowables & HasItem("Horn")
AirTail: Logic = carrying.NoThrowables & HasItem("Aerial Tail")
GroundTail: Logic = carrying.NoThrowables & HasItem("Grounded Tail")
Climb: Logic = carrying.NoThrowables & HasItem("Climb")

CanClimbPlantedTree = HasItem("Climb") & carrying.Apple & carrying._ClimbPlantedTree()