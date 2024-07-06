from ...logic import lazy_region, Entrance, Region
from ...logic import item, tech, carrying, event
from ...logic import Any

class KerringtonDoor(Entrance): pass

@lazy_region
def Main(r: Region):
  r.locations = {
    "Heart - Generators Puzzle": Any(
      item.air_tail, item.ground_tail,
      carrying.apple, carrying.bubble_conch,
      item.horn & item.double_jump
    ),

    "Egg: Mr. Kerrington's Heart": Any(
      tech.any_super_jump,
      event.Collected("Unclog Kerrington's Heart")
    )
  }

  from . import Kerrington

  r.entrances = [
    KerringtonDoor.define(Kerrington.HeartDoor)
  ]
