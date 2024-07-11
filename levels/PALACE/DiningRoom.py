from ...logic import lazy_region, Region, Entrance, Any
from ...logic import item, carrying, difficulty, tech, event

area_path = "PALACE/Dining Room"

class ValleyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromDiningRoomToPalace"
  dest_path = f"{area_path}/Warps/DestFromPalaceToDiningRoom"

@lazy_region
def Main(r: Region):
  r.locations = {
    "Palace Dining Room - Preston": item.horn
  }

  from . import Valley

  r.entrances = [
    ValleyDoor.define(Valley.DiningRoomDoor)
  ]

  r.region_connections = {
    InitialPlatforms: Any(
      event.Collected("Raise Dining Room Platform"),
      tech.any_super_jump,

      item.double_jump & Any(
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump & item.high_jump,
        item.wings & tech.bubble_jump_and_recoil
      )
    )
  }

@lazy_region
def InitialPlatforms(r: Region):
  r.region_connections = {
    Chandelier: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      item.wings,
      tech.air_tail_jump,
      tech.ground_tail_jump,
      item.horn,
      tech.bubble_jump,
      item.sprint,
    )
  }

@lazy_region
def Chandelier(r: Region):
  r.locations = {
    "Egg: Palace Dining Room": None,
    "Card: Palace Dining Room - Top": Any(
      item.wings,
      tech.bubble_jump,
      item.double_jump,
      tech.air_tail_jump,
      item.air_tail & item.roll,
      tech.ground_tail_jump & difficulty.hard,
      item.sprint & difficulty.hard,
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
    )
  }

  r.region_connections = {
    Main: None
  }
