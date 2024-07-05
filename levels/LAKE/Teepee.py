from ...logic import lazy_region, Region, Entrance
from ...logic.objects import EntranceType

class FrontDoor(Entrance): pass
class Topside(Entrance): pass

@lazy_region
def Main(r: Region):
  from . import LostleafLake
  r.entrances = [
    FrontDoor.define(LostleafLake.TeepeeFrontDoor),

    Topside.define(
      default_connection = LostleafLake.TeepeeTopside,
      type = EntranceType.ENTRANCE
    )
  ]
