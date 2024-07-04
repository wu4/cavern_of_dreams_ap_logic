from ...logic.objects import lazy_region, Region, Entrance, InternalEvent
from ...logic import item, carrying
from ...logic import event

class SunCavernDoor(Entrance): pass
class LostleafLakeDoor(Entrance): pass
class GalleryLobbyDoor(Entrance): pass
class SunCavernTeleport(Entrance): pass

# this wall is unique in that it can be broken from both directions
class BrokeHiddenWall(InternalEvent): pass

# give it an associated region with a dead-end
@lazy_region
def BreakHiddenWall(r: Region):
  r.locations = {
    BrokeHiddenWall: None
  }

@lazy_region
def Main(r: Region):
  r.locations = {
    "Shroom: Lostleaf Lobby - Bridge 1": None,
    "Shroom: Lostleaf Lobby - Bridge 2": None,
    "Shroom: Lostleaf Lobby - Bridge 3": None
  }

  from . import SunCavern
  from ..LAKE import LostleafLake

  r.entrances = [
    SunCavernDoor.define(SunCavern.LostleafLobbyDoor),

    LostleafLakeDoor.define(LostleafLake.LostleafLobbyDoor),

    SunCavernTeleport.define(
      default_connection = SunCavern.LostleafLobbyTeleport,
      rule = event.Collected("Open Lake Lobby Teleport")
    )
  ]

  r.region_connections = {
    BreakHiddenWall: CanBreakHiddenWall,
    HiddenDoorway: event.Collected(BrokeHiddenWall),

    Trees: None # difficulty.Intermediate | templates.HighJumpObstacle
  }

@lazy_region
def Trees(r: Region):
  r.locations = {
    "Shroom: Lostleaf Lobby - Trees 1": None,
    "Shroom: Lostleaf Lobby - Trees 2": None,
    "Shroom: Lostleaf Lobby - Trees 3": None,

    "Egg: Lostleaf Lobby - Branches": None,

    "Card: Lostleaf Lobby - Branches": None,
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def HiddenDoorway(r: Region):
  from . import GalleryLobby

  r.entrances = [
    GalleryLobbyDoor.define(GalleryLobby.LostleafLobbyDoor)
  ]

  r.region_connections = {
    BreakHiddenWall: CanBreakHiddenWall,
    Main: event.Collected(BrokeHiddenWall)
  }

CanBreakHiddenWall = item.ground_tail | item.air_tail | carrying.apple | carrying.bubble_conch
