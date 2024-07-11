from ...logic import lazy_region, Region, Entrance, Any, CarryableLocation
from ...logic import item, carrying, tech, event

area_path = "PALACE/Sanctum"

class PalaceDoor(Entrance):
  is_underwater = True
  warp_path = f"{area_path}/Warps/WarpFromSanctumToPalace"
  dest_path = f"{area_path}/Warps/DestFromPalaceToSanctum"
class ValleyDoor(Entrance):
  # [sic]
  warp_path = f"{area_path}/Warps/WarpFromSanctumToValleyTop"
  dest_path = f"{area_path}/Warps/DestFromValleyToSanctum"

class BubbleConch(CarryableLocation): carryable = "Bubble Conch"

@lazy_region
def Main(r: Region):
  r.locations = {
    BubbleConch: item.carry,

    "Heaven's Path - Bottom Preston": item.swim
  }

  r.region_connections = {
    BubbleClimb: event.Collected("Open Heaven's Path Exit"),
    PalaceEntryway: item.swim,
    RaceStart: event.Collected("Open Heaven's Path Race Entrance") & item.swim & Any(
      tech.any_super_jump,
      tech.ground_tail_jump & item.high_jump & item.wings & tech.ability_toggle & item.double_jump,
      item.sprint,
      carrying.bubble_conch,
      carrying.shelnerts_fish,
    )
  }

@lazy_region
def PalaceEntryway(r: Region):
  from . import Palace

  r.entrances = [
    PalaceDoor.define(Palace.SanctumDoor)
  ]

  r.region_connections = {
    Main: None
  }

@lazy_region
def RaceStart(r: Region):
  r.locations = {
    "Heaven's Path - Finished Race": item.sprint | carrying.bubble_conch
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def BubbleClimb(r: Region):
  r.region_connections = {
    Main: event.Collected("Open Heaven's Path Exit"),
    ValleyEntryway: item.swim & Any(
      item.sprint,
      carrying.bubble_conch,
      carrying.shelnerts_fish,
      carrying.mr_kerringtons_wings,
      item.double_jump,
      item.wings,
      tech.bubble_jump
    )
  }

@lazy_region
def ValleyEntryway(r: Region):
  from . import Valley

  r.entrances = [
    ValleyDoor.define(Valley.SanctumDoor)
  ]

  r.region_connections = {
    BubbleClimb: None
  }
