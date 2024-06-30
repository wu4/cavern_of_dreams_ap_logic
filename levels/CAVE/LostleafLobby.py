from typing import override

from ...logic.objects import Region, Entrance, InternalEvent
from ...logic import item, carrying
from ...logic import event

class SunCavernDoor(Entrance): pass
class LostleafLakeDoor(Entrance): pass
class GalleryLobbyDoor(Entrance): pass
class SunCavernTeleport(Entrance): pass

# this wall is unique in that it can be broken from both directions
class BrokeHiddenWall(InternalEvent): pass

# give it an associated region with a dead-end
class BreakHiddenWall(Region):
  locations = {
    BrokeHiddenWall: None
  }

  @override
  @classmethod
  def load(cls): pass

class Main(Region):
  locations = {
    "Shroom: Lostleaf Lobby - Bridge 1": None,
    "Shroom: Lostleaf Lobby - Bridge 2": None,
    "Shroom: Lostleaf Lobby - Bridge 3": None
  }

  @override
  @classmethod
  def load(cls):
    from . import SunCavern
    from ..LAKE import LostleafLake

    cls.entrances = [
      SunCavernDoor.define(SunCavern.LostleafLobbyDoor),

      LostleafLakeDoor.define(LostleafLake.LostleafLobbyDoor),

      SunCavernTeleport.define(
        default_connection = SunCavern.LostleafLobbyTeleport,
        rule = event.Collected("Open Lake Lobby Teleport")
      )
    ]

    cls.region_connections = {
      BreakHiddenWall: CanBreakHiddenWall,
      HiddenDoorway: event.Collected(BrokeHiddenWall),

      Trees: None # difficulty.Intermediate | templates.HighJumpObstacle
    }

class Trees(Region):
  locations = {
    "Shroom: Lostleaf Lobby - Trees 1": None,
    "Shroom: Lostleaf Lobby - Trees 2": None,
    "Shroom: Lostleaf Lobby - Trees 3": None,

    "Egg: Lostleaf Lobby - Branches": None,

    "Card: Lostleaf Lobby - Branches": None,
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None
    }

class HiddenDoorway(Region):
  @override
  @classmethod
  def load(cls):
    from . import GalleryLobby

    cls.entrances = [
      GalleryLobbyDoor.define(GalleryLobby.LostleafLobbyDoor)
    ]

    cls.region_connections = {
      BreakHiddenWall: CanBreakHiddenWall,
      Main: event.Collected(BrokeHiddenWall)
    }

CanBreakHiddenWall = item.ground_tail | item.air_tail | carrying.apple | carrying.bubble_conch
