from ...logic import *

class Main(Region): pass

class ArmadaLobbyDoor(Entrance): pass
class SkyDoor(Entrance): pass

from ..CAVE import ArmadaLobby as _ArmadaLobby
from . import Sky as _Sky

regions = [
  Main.define(
    locations = {
      "Shroom: Armada Entry Drone - Ledges 1": None,
      "Shroom: Armada Entry Drone - Ledges 2": None,
      "Shroom: Armada Entry Drone - Ledges 3": None,
      "Shroom: Armada Entry Drone - Ledges 4": None,
      "Shroom: Armada Entry Drone - Ledges 5": None,
      "Shroom: Armada Entry Drone - Ledges 6": None,
      "Shroom: Armada Entry Drone - Ledges 7": None,
      "Shroom: Armada Entry Drone - Ledges 8": None
    },

    entrances = [
      ArmadaLobbyDoor.define(
        default_connection = _ArmadaLobby.EarthDroneCannonShot,
        rule = None
      ),
      SkyDoor.define(
        default_connection = _Sky.EarthDroneDoor,
        rule = None
      )
    ]
  )
]
