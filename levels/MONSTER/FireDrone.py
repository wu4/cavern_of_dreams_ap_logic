from ...logic import lazy_region, Entrance, Region
from ...logic import item, carrying

class SkyDoor(Entrance): pass

@lazy_region
def Main(r: Region):
  r.locations = {
    "Egg: Fire Drone": item.bubble | carrying.medicine
  }

  from . import Sky

  r.entrances = [
    SkyDoor.define(Sky.FireDroneDoor)
  ]
