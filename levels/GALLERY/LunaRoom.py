from ...logic import lazy_region, Region, Entrance

area_path = "GALLERY/Secret Room"

class WaterLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromSecretRoomToWaterLobby"
  dest_path = f"{area_path}/Warps/DestFromWaterLobbyToSecretRoom"

@lazy_region
def LunaHouse(r: Region):
  from . import WaterLobby

  r.entrances = [
    WaterLobbyDoor.define(WaterLobby.LunaRoomDoor)
  ]
