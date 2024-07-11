from typing import override

from ...logic import Entrance, Region

area_path = "MONSTER/DroneEarth"

class ArmadaLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromDroneEarthToMonsterLobby"
  dest_path = f"{area_path}/Warps/DestFromMonsterLobbyToDroneEarth"
class SkyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromDroneEarthToSky"
  dest_path = f"{area_path}/Warps/DestFromSkyToDroneEarth"

class Main(Region):
  locations = {
    "Shroom: Armada Entry Drone - Ledges 1": None,
    "Shroom: Armada Entry Drone - Ledges 2": None,
    "Shroom: Armada Entry Drone - Ledges 3": None,
    "Shroom: Armada Entry Drone - Ledges 4": None,
    "Shroom: Armada Entry Drone - Ledges 5": None,
    "Shroom: Armada Entry Drone - Ledges 6": None,
    "Shroom: Armada Entry Drone - Ledges 7": None,
    "Shroom: Armada Entry Drone - Ledges 8": None
  }

  @override
  @classmethod
  def load(cls):
    from ..CAVE import ArmadaLobby
    from . import Sky

    cls.entrances = [
      ArmadaLobbyDoor.define(
        default_connection = ArmadaLobby.EarthDroneCannonShot,
        rule = None
      ),
      SkyDoor.define(
        default_connection = Sky.EarthDroneDoor,
        rule = None
      )
    ]
