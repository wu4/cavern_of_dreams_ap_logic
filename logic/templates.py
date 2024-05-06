from . import Any
from .item import HighJump, Horn, DoubleJump
from .tech import AnySuperJump, GroundTailJump, AirTailJump

HighJumpObstacle = Any(
  HighJump,
  Horn,
  DoubleJump,
  GroundTailJump,
  AirTailJump,
  AnySuperJump
)