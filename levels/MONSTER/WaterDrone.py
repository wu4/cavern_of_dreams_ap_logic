from ...logic import lazy_region, Entrance, Region

class SkyDoor(Entrance): pass

@lazy_region
def Main(r: Region):
  from . import Sky

  r.entrances = [
    SkyDoor.define(Sky.WaterDroneDoor)
  ]
