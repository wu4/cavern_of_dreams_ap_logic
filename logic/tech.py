from . import Logic, MaybeLogic as _MaybeLogic, All, Any
from .has import HasWings, HasBubble, HasRoll, HasAirTail, HasGroundTail, NoTempItems, HasSuperBounce, HasSuperBubbleJump

from typing import TypeAlias, Literal

TechType: TypeAlias = Literal[
  "ejection_launch",
  "z_target",
  "momentum_cancel",
  "damage_boost",
  "ability_toggle",
  "out_of_bounds",
  "roll_disjoint",
  "standable_terrain",

  "tail_jump",
  "hover_jump",
  "hover_shoot",
  "super_bubble_jump",
  "super_bounce",
  "bubble_jump",
]

class Tech(Logic):
  def __str__(self) -> str:
    return f"Tech: {self.tech}"
  
  def __init__(self, tech: TechType) -> None:
    self.tech = tech
    super().__init__()

CanHoverJump: Logic = Tech("hover_jump") & HasWings
CanBubbleJump: Logic = Tech("bubble_jump") & HasBubble
CanHoverShoot: Logic = Tech("hover_shoot") & HasWings & HasBubble
CanSuperBounce: Logic = Tech("super_bounce") & HasSuperBounce & HasRoll & HasAirTail
CanSuperBubbleJump: Logic = Tech("super_bubble_jump") & HasSuperBubbleJump & HasRoll & HasBubble
def CanRollDisjoint(requires_tail: bool = False) -> Logic:
  ret = Tech("roll_disjoint") & HasRoll
  if requires_tail:
    ret &= (HasGroundTail | HasAirTail)
  return ret

def CanDamageBoost(logic: _MaybeLogic = None) -> Logic:
  return All(
    NoTempItems,
    Tech("damage_boost") if logic is None else Tech("damage_boost") & logic
  )

def CanTailJump(groundedExtraLogic: Logic | None = None, aerialExtraLogic: Logic | None = None) -> Logic:
  return Tech("tail_jump") & Any(
    HasGroundTail if groundedExtraLogic is None else (HasGroundTail & groundedExtraLogic),
    HasAirTail if aerialExtraLogic is None else (HasAirTail & aerialExtraLogic),
  )

CanSuperJump = CanSuperBounce | CanSuperBubbleJump