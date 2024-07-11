from ...logic import lazy_region, Entrance, Region

area_path = "MONSTER/DroneWater"

class SkyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromDroneWaterToSky"
  dest_path = f"{area_path}/Warps/DestFromSkyToDroneWater"

@lazy_region
def Main(r: Region):
  from . import Sky

  r.entrances = [
    SkyDoor.define(Sky.WaterDroneDoor)
  ]
