from . import Logic, Any
from .has import HasGroundTail, HasAirTail, HasRoll, HasHorn, Carrying

def Whackable(
  ground_tail_works: bool = False,
  air_tail_works: bool = False,
  roll_works: bool = False,
  throwable_works: bool = False,
  horn_works: bool = False
) -> Logic:
  accum = []
  if ground_tail_works: accum.append(HasGroundTail)
  if air_tail_works: accum.append(HasAirTail)
  if roll_works: accum.append(HasRoll & (HasGroundTail | HasAirTail))
  if throwable_works: accum.append(Carrying("Apple") | Carrying("Bubble Conch"))
  if horn_works: accum.append(HasHorn)
  return Any(*accum)