from . import Any
from .item import HighJump, Horn, DoubleJump
from .tech import CanTailJump, SuperJump

HighJumpObstacle = Any(
  HasHighJump,
  HasHorn,
  HasDoubleJump,
  CanTailJump(),
  CanSuperJump
)