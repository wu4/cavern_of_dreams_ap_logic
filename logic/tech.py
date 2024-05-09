from . import Logic
from . import item, carrying

from typing import TypeAlias, Literal, override

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
  @override
  def __str__(self) -> str:
    return f"Tech: {self.tech}"

  def __init__(self, tech: TechType) -> None:
    self.tech = tech
    super().__init__()

ejection_launch: Logic = Tech("ejection_launch")
z_target: Logic = Tech("z_target")
momentum_cancel: Logic = Tech("momentum_cancel")
ability_toggle: Logic = Tech("ability_toggle")
out_of_bounds: Logic = Tech("out_of_bounds")

hover_jump: Logic = Tech("hover_jump") & item.wings
bubble_jump: Logic = Tech("bubble_jump") & item.bubble
hover_shoot: Logic = Tech("hover_shoot") & item.wings & item.bubble
super_bounce: Logic = Tech("super_bounce") & item.SuperBounce & item.roll & item.air_tail
super_bubble_jump: Logic = Tech("super_bubble_jump") & item.SuperBubbleJump & item.roll & item.bubble

def roll_disjoint(requires_tail: bool = False) -> Logic:
  ret = Tech("roll_disjoint") & item.roll
  if requires_tail:
    ret &= (item.ground_tail | item.air_tail)
  return ret

DamageBoost: Logic = Tech("damage_boost") & carrying.NoTempItems
# def DamageBoost(logic: MaybeLogic = None) -> Logic:
#   ret = Tech("damage_boost") & carrying.NoTempItems
#   if logic is not None: ret &= logic
#   return ret

ground_tail_jump: Logic = Tech("ground_tail_jump") & item.ground_tail
air_tail_jump: Logic = Tech("air_tail_jump") & item.air_tail

any_super_jump = super_bounce | super_bubble_jump
