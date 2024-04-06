from __future__ import annotations
from typing import TypeAlias, Literal

from . import Logic
from .objects import InternalEvent
from ..generated import AnyItem

HasType: TypeAlias = AnyItem | type[InternalEvent]

class Has(Logic):
  def __str__(self) -> str:
    return f"Has {self.has}"
  
  def __init__(self, has: HasType) -> None:
    self.has = has
    super().__init__()

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

NoThrowables = _NoThrowables()

NoJesterBoots = _NoJesterBoots()

NoTempItems = NoThrowables & NoJesterBoots

HasHorn: Logic = NoThrowables & Has("Horn")
HasAirTail: Logic = NoThrowables & Has("Aerial Tail")
HasGroundTail: Logic = NoThrowables & Has("Grounded Tail")
HasClimb: Logic = NoThrowables & Has("Climb")

HasWings: Logic = Has("Wings")
HasDoubleJump: Logic = Has("Double Jump")
HasBubble: Logic = Has("Bubble")
HasFlight: Logic = Has("Flight")
HasRoll: Logic = Has("Roll")
HasSprint: Logic = Has("Sprint")
HasHighJump: Logic = Has("High Jump")
HasSwim: Logic = Has("Swim")
HasCarry: Logic = Has("Carry")
HasSuperBounce: Logic = Has("Super Bounce")
HasSuperBubbleJump: Logic = Has("Super Bubble Jump")
HasAirSwim: Logic = Has("Air Swim")

CanClimbPlantedTree = Has("Climb") & Carrying("Apple") & _ClimbPlantedTree()