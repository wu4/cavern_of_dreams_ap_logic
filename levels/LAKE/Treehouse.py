from ...logic import lazy_region, Region, Entrance, Any
from ...logic import tech, event

class LostleafFrontDoor(Entrance): pass
class LostleafBackDoor(Entrance): pass

@lazy_region
def Main(r: Region):
  r.locations = {
    "Shroom: Treehouse - Corners 1": None,
    "Shroom: Treehouse - Corners 2": None,
    "Shroom: Treehouse - Corners 3": None,
    "Shroom: Treehouse - Corners 4": None,
    "Shroom: Treehouse - Corners 5": None,
    "Shroom: Treehouse - Corners 6": None,

    "Card: Treehouse - Top": None,

    "Treehouse - Fish Food": None
  }

  from . import LostleafLake

  r.entrances = [
    LostleafFrontDoor.define(
      default_connection = LostleafLake.TreehouseFrontDoor,
      rule = Any(
        event.Collected("Open Treehouse"),
        tech.roll_disjoint
      )
    ),

    LostleafBackDoor.define(
      default_connection = LostleafLake.TreehouseBackDoor
    )
  ]
