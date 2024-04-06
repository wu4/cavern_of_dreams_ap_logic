from . import Any
from .has import HasHighJump, HasHorn, HasDoubleJump
from .tech import CanTailJump, CanSuperJump

HighJumpObstacle = Any(
  HasHighJump,
  HasHorn,
  HasDoubleJump,
  CanTailJump(),
  CanSuperJump
)