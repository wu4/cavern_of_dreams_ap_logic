from ...logic import lazy_region, Entrance, Region
from ...logic import item, carrying

area_path = "MONSTER/DroneFire"

class SkyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromDroneFireToSky"
  dest_path = f"{area_path}/Warps/DestFromSkyToDroneFire"

@lazy_region
def Main(r: Region):
  r.locations = {
    "Egg: Fire Drone": item.bubble | carrying.medicine
  }

  from . import Sky

  r.entrances = [
    SkyDoor.define(Sky.FireDroneDoor)
  ]
