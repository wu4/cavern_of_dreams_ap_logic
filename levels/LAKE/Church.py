from ...logic import lazy_region, Region, Entrance, Any
from ...logic import item, tech, carrying, event

area_path = "LAKE/Church"

class LostleafLakeDoor(Entrance):
  is_dest_underwater = True
  warp_path = f"{area_path}/Warps/WarpFromChurchToLake"
  dest_path = f"{area_path}/Warps/DestFromLakeToChurch"

@lazy_region
def Main(r: Region):
  r.locations = {
    "Shroom: Church - Pews 1": None,
    "Shroom: Church - Pews 2": None,
    "Shroom: Church - Pews 3": None,
    "Shroom: Church - Pews 4": None,

    "Church - Angel Statue Puzzle": Any(
      item.air_tail | item.ground_tail,
      carrying.apple | carrying.bubble_conch
    ),

    "Card: Church - Top": Any(
      item.wings & Any(
        item.double_jump,
        tech.bubble_jump_and_recoil
      ),
      item.sprint,
      carrying.bubble_conch | carrying.shelnerts_fish,
      carrying.jester_boots & tech.super_bubble_jump & item.roll
    )
  }

  from . import LostleafLake

  r.entrances = [
    LostleafLakeDoor.define(LostleafLake.ChurchDoor)
  ]

  r.region_connections = {
    Basement: event.Collected("Open Church Basement")
  }

@lazy_region
def Basement(r: Region):
  r.locations = {
    "Egg: Church - Below the Angel Statues": None
  }

  r.region_connections = {
    Main: None
  }
