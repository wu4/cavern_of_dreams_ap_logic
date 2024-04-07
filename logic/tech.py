from . import Logic, MaybeLogic as _MaybeLogic, All, Any
from . import item
# from .has import HasWings, HasBubble, HasRoll, HasAirTail, HasGroundTail, NoTempItems, HasSuperBounce, HasSuperBubbleJump

from typing import TypeAlias, Literal

TechType: TypeAlias = Literal[
  "ejection_launch",
  "z_target",
  "momentum_cancel",
  "damage_boost",
  "ability_toggle",
  "out_of_bounds",
  "roll_disjoint",

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

EjectionLaunch: Logic = Tech("ejection_launch")
ZTarget: Logic = Tech("z_target")
MomentumCancel: Logic = Tech("momentum_cancel")
AbilityToggle: Logic = Tech("ability_toggle")
OutOfBounds: Logic = Tech("out_of_bounds")

HoverJump: Logic = Tech("hover_jump") & item.Wings
BubbleJump: Logic = Tech("bubble_jump") & item.Bubble
HoverShoot: Logic = Tech("hover_shoot") & item.Wings & item.Bubble
SuperBounce: Logic = Tech("super_bounce") & item.SuperBounce & item.Roll & item.AirTail
SuperBubbleJump: Logic = Tech("super_bubble_jump") & item.SuperBubbleJump & item.Roll & item.Bubble
SuperJump: Logic = SuperBounce | SuperBubbleJump

def RollDisjoint(requires_tail: bool = False) -> Logic:
  ret = Tech("roll_disjoint") & item.Roll
  if requires_tail:
    ret &= (item.GroundTail | item.AirTail)
  return ret

def DamageBoost(logic: _MaybeLogic = None) -> Logic:
  return All(
    item.NoTempItems,
    Tech("damage_boost") if logic is None else Tech("damage_boost") & logic
  )

def TailJump(groundedExtraLogic: Logic | None = None, aerialExtraLogic: Logic | None = None) -> Logic:
  return Tech("tail_jump") & Any(
    item.GroundTail if groundedExtraLogic is None else (item.GroundTail & groundedExtraLogic),
    item.AirTail if aerialExtraLogic is None else (item.AirTail & aerialExtraLogic),
  )