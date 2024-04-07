from . import Logic, Any
from . import item, carrying

def Whackable(
  ground_tail_works: bool = False,
  air_tail_works: bool = False,
  roll_works: bool = False,
  throwable_works: bool = False,
  horn_works: bool = False
) -> Logic:
  accum = []
  if ground_tail_works: accum.append(item.GroundTail)
  if air_tail_works: accum.append(item.AirTail)
  if roll_works: accum.append(item.Roll & (item.GroundTail | item.AirTail))
  if throwable_works: accum.append(carrying.Apple | carrying.BubbleConch)
  if horn_works: accum.append(item.Horn)
  return Any(*accum)