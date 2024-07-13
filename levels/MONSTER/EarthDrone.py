from ...logic import lazy_region, Entrance, Region

area_path = "MONSTER/DroneEarth"

class ArmadaLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromDroneEarthToMonsterLobby"
  dest_path = f"{area_path}/Warps/DestFromMonsterLobbyToDroneEarth"
class SkyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromDroneEarthToSky"
  dest_path = f"{area_path}/Warps/DestFromSkyToDroneEarth"

@lazy_region
def Main(r: Region):
  r.locations = {
    "Shroom: Armada Entry Drone - Ledges 1": None,
    "Shroom: Armada Entry Drone - Ledges 2": None,
    "Shroom: Armada Entry Drone - Ledges 3": None,
    "Shroom: Armada Entry Drone - Ledges 4": None,
    "Shroom: Armada Entry Drone - Ledges 5": None,
    "Shroom: Armada Entry Drone - Ledges 6": None,
    "Shroom: Armada Entry Drone - Ledges 7": None,
    "Shroom: Armada Entry Drone - Ledges 8": None
  }

  from ..CAVE import ArmadaLobby
  from . import Sky

  r.entrances = [
    ArmadaLobbyDoor.define(ArmadaLobby.EarthDroneCannonShot),
    SkyDoor.define(Sky.EarthDroneDoor)
  ]
