from ...logic import lazy_region, Region, Entrance

area_path = "LAKE/Tent"

class FrontDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromTentToLake"
  dest_path = f"{area_path}/Warps/DestFromLakeToTent"
class Topside(Entrance):
  dest_path = f"{area_path}/Warps/DestFromLakeToTentTop"

@lazy_region
def Main(r: Region):
  from . import LostleafLake
  r.entrances = [
    FrontDoor.define(LostleafLake.TeepeeFrontDoor),

    Topside.define(LostleafLake.TeepeeTopside)
  ]
