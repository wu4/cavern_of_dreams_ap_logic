from . import Any
from .item import high_jump, horn, double_jump
from .tech import any_super_jump, ground_tail_jump, air_tail_jump

high_jump_obstacle = Any(
  high_jump,
  horn,
  double_jump,
  ground_tail_jump,
  air_tail_jump,
  any_super_jump
)
