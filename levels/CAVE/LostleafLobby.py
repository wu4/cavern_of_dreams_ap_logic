from ...logic import Any, All, Logic
from ...logic.objects import Region, Entrance, InternalEvent
from ...logic.whackable import Whackable
from ...logic import item, event

class Main(Region): pass
class Trees(Region): pass
class HiddenDoorway(Region): pass

class SunCavernDoor(Entrance): pass
class LostleafLakeDoor(Entrance): pass
class GalleryLobbyDoor(Entrance): pass
class SunCavernTeleport(Entrance): pass

# this wall is unique in that it can be broken from both directions
class BrokeHiddenWall(InternalEvent): pass
# give it an associated region with a dead-end
class BreakHiddenWall(Region): pass
CanBreakHiddenWall: Logic = Whackable(
  ground_tail_works = True,
  air_tail_works = True,
  roll_works = True,
  throwable_works = True
)

from . import SunCavern as _SunCavern
from . import GalleryLobby as _GalleryLobby
from ..LAKE import LostleafLake as _LostleafLake

regions = [
  Main.define(
    locations = {
      "Shroom: Lostleaf Lobby - Bridge 1": None,
      "Shroom: Lostleaf Lobby - Bridge 2": None,
      "Shroom: Lostleaf Lobby - Bridge 3": None
    },

    entrances = [
      SunCavernDoor.define(_SunCavern.LostleafLobbyDoor),

      LostleafLakeDoor.define(_LostleafLake.LostleafLobbyDoor),

      SunCavernTeleport.define(
        to = _SunCavern.LostleafLobbyTeleport,
        rule = event.Collected("Open Lake Lobby Teleport")
      )
    ],

    region_connections = {
      BreakHiddenWall: CanBreakHiddenWall,
      HiddenDoorway: event.Collected(BrokeHiddenWall),

      Trees: None # difficulty.Intermediate | templates.HighJumpObstacle
    },
  ),
  
  BreakHiddenWall.define(
    locations = {
      BrokeHiddenWall: None
    }
  ),

  Trees.define(
    locations = {
      "Shroom: Lostleaf Lobby - Trees 1": None,
      "Shroom: Lostleaf Lobby - Trees 2": None,
      "Shroom: Lostleaf Lobby - Trees 3": None,
      
      "Egg: Lostleaf Lobby - Branches": None,
      
      "Card: Lostleaf Lobby - Branches": None,
    },

    region_connections = {
      Main: None
    }
  ),
  
  HiddenDoorway.define(
    entrances = [
      GalleryLobbyDoor.define(_GalleryLobby.lostleaf_lobby_door)
    ],

    region_connections = {
      BreakHiddenWall: CanBreakHiddenWall,
      Main: event.Collected(BrokeHiddenWall)
    }
  )
]
