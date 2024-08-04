from ...logic import lazy_region, Region, Entrance, InternalEvent, Any
from ...logic import item, carrying, tech, event, difficulty, templates

area_path = "GALLERY/Fire Lobby"

class FoyerDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromFireLobbyToFoyer"
  dest_path = f"{area_path}/Warps/DestFromFoyerToFireLobby"

class EarthLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFireToEarth"
  dest_path = f"{area_path}/Warps/DestEarthToFire"

class ChalicePainting(Entrance):
  painting_path = f"{area_path}/Objects/PaintingWarpChalice"
  warp_path = f"{painting_path}/WarpCutscene/WarpEvent"
  dest_path = f"{painting_path}/DestFromPaintingChalice"

class DouseRaceFlame(InternalEvent): pass

@lazy_region
def Main(r: Region):
  r.locations = {
    DouseRaceFlame: item.bubble | carrying.medicine,

    "Fire Lobby Hoops": event.Collected(DouseRaceFlame) & Any(
      item.wings,
      carrying.mr_kerringtons_wings,
      # tech.z_target & tech.bubble_jump_and_recoil & item.double_jump,
      # This is probably possible, but I decided to move on from proving it for
      # the greater good. Maybe someday I'll get a clip of it, but I like the
      # idea of this project coming to a release a bit more.
    ),

    "Card: Fire Lobby - Frying Pans": Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      (item.bubble | carrying.no_temp_items) & tech.any_super_jump,
      item.horn & item.bubble,
      tech.bubble_jump & tech.momentum_cancel & carrying.no_temp_items,
      item.wings & Any(
        item.bubble,
        carrying.medicine,
        carrying.no_temp_items
      )
    )
  }

  from . import Foyer

  r.entrances = [
    FoyerDoor.define(Foyer.FireLobbyDoor)
  ]

  r.region_connections = {
    ChalicePlatform: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings & tech.wing_jump,
      tech.any_super_jump,
      event.Collected("Extend Fire Lobby Frying Pans") & carrying.no_temp_items,
    ),

    FishPlatform: Any(
      item.climb,
      tech.ground_tail_jump & item.double_jump & item.wings,
    ),

    EarthLobbyEntryway: Any(
      event.Collected("Extend Fire Lobby Tongue Platform"),
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      tech.super_bubble_jump,
      item.wings,
      tech.bubble_jump & Any(
        tech.ground_tail_jump,
        item.double_jump,
      ),
      item.air_tail & item.roll,
      item.climb & Any(
        tech.ejection_launch & Any(
          difficulty.hard,
          difficulty.intermediate & tech.bubble_jump
        )
      )
    ),

    ClimbToKerringtonPaintingPlatform: Any(
      carrying.mr_kerringtons_wings,
      tech.air_tail_jump,
      tech.ground_tail_jump,
      item.double_jump,
      item.sprint,
      tech.bubble_jump,
      item.roll,
      item.horn
    ),

    KerringtonPaintingPlatform: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
    )
  }

@lazy_region
def ClimbToKerringtonPaintingPlatform(r: Region):
  # separated so throwable logic can work here
  r.region_connections = {
    KerringtonPaintingPlatform: item.climb
  }

@lazy_region
def FishPlatform(r: Region):
  r.locations = {
    "Fire Lobby - Shelnert's Fish": None
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def EarthLobbyEntryway(r: Region):
  r.locations = {
    "Fire Lobby Preston": None
  }

  from . import EarthLobby

  r.entrances = [
    EarthLobbyDoor.define(EarthLobby.FireLobbyDoor)
  ]

  r.region_connections = {
    Main: None
  }

@lazy_region
def KerringtonPaintingPlatform(r: Region):
  r.locations = {
    "Fire Lobby - Mr. Kerrington's Painting": carrying.mr_kerringtons_wings,
    "Egg: Fire Lobby - Mr. Kerrington Painting": event.Collected("Open Mr. Kerrington Painting Gate")
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def ChalicePlatform(r: Region):
  from . import Chalice

  r.entrances = [
    ChalicePainting.define(
      default_connection = Chalice.FireLobbyDoor,
      rule = carrying.jester_boots | templates.high_jump_obstacle | item.sprint
    )
  ]

  r.region_connections = {
    Main: None,
    FishPlatform: Any(
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
      tech.wing_jump & difficulty.intermediate,
      item.wings & Any(
        item.climb,
        item.sprint,
        tech.air_tail_jump,
        tech.ground_tail_jump
      )
    ),
    KerringtonPaintingPlatform: Any(
      carrying.mr_kerringtons_wings,
      carrying.jester_boots
    )
  }
