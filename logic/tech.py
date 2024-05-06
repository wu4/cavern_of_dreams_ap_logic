from . import Logic, MaybeLogic, All, Any
from . import item, carrying

from typing import TypeAlias, Literal

TechType: TypeAlias = Literal[
  "ejection_launch",
  "z_target",
  "momentum_cancel",
  "damage_boost",
  "ability_toggle",
  "out_of_bounds",
  "roll_disjoint",

  "ground_tail_jump",
  "air_tail_jump",
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

def RollDisjoint(requires_tail: bool = False) -> Logic:
  ret = Tech("roll_disjoint") & item.Roll
  if requires_tail:
    ret &= (item.GroundTail | item.AirTail)
  return ret

DamageBoost: Logic = Tech("damage_boost") & carrying.NoTempItems
# def DamageBoost(logic: MaybeLogic = None) -> Logic:
#   ret = Tech("damage_boost") & carrying.NoTempItems
#   if logic is not None: ret &= logic
#   return ret

GroundTailJump: Logic = Tech("ground_tail_jump") & item.GroundTail
AirTailJump: Logic = Tech("air_tail_jump") & item.AirTail

AnySuperJump = SuperBounce | SuperBubbleJump