from ...logic.objects import lazy_region, Region, Entrance, InternalEvent
from ...logic import item, carrying
from ...logic import event

area_path = "CAVE/Lake Lobby"

class SunCavernDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromLakeLobbyToCave"
  dest_path = f"{area_path}/Warps/DestFromCaveToLakeLobby"
class LostleafLakeDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromLakeLobbyToLake"
  dest_path = f"{area_path}/Warps/DestFromLakeToLakeLobby"
class GalleryLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromLakeLobbyToGalleryLobby"
  dest_path = f"{area_path}/Warps/DestFromGalleryLobbyToLakeLobby"
class SunCavernTeleport(Entrance):
  warp_path = f"{area_path}/Warps/Portal"
  dest_path = f"{warp_path}/DestFromPortal???"

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
      rule = event.Collected("Open Lake Lobby Teleport") & carrying.no_jester_boots
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
