from ...logic import lazy_region, Region, Entrance, InternalEvent, Any
from ...logic import item, carrying, tech, event

area_path = "PALACE/Palace"

class FrontDoor(Entrance):
  is_dest_underwater = True
  warp_path = f"{area_path}/Warps/WarpFromPalaceToValley"
  dest_path = f"{area_path}/Warps/DestFromValleyToPalace"
class SanctumDoor(Entrance):
  is_dest_underwater = True
  warp_path = f"{area_path}/Warps/WarpFromPalaceToSanctum"
  dest_path = f"{area_path}/Warps/DestFromSanctumToPalace"
class BasementDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromPalaceToAbyss"
  dest_path = f"{area_path}/Warps/DestFromAbyssToPalace"

class KnockedPillarsDown(InternalEvent): pass

@lazy_region
def Main(r: Region):
  r.locations = {
    "Shroom: Palace Interior - Palace Back 1": None,
    "Shroom: Palace Interior - Palace Back 2": None,
    "Shroom: Palace Interior - Palace Back 3": None,
    "Shroom: Palace Interior - Palace Back 4": None,
    "Shroom: Palace Interior - Palace Back 5": None,
    "Shroom: Palace Interior - Palace Back 6": None,

    "Shroom: Palace Interior - Star Puzzle 1": None,
    "Shroom: Palace Interior - Star Puzzle 2": None,
    "Shroom: Palace Interior - Star Puzzle 3": None,

    "Card: Palace": Any(
      carrying.bubble_conch | carrying.shelnerts_fish,
      item.sprint & Any(
        item.double_jump,
        item.horn
      )
    ),

    "Palace Interior - Seastar Puzzle": item.horn,

    KnockedPillarsDown: item.horn
  }

  from . import Valley

  r.entrances = [
    FrontDoor.define(Valley.PalaceFrontDoor)
  ]

  r.region_connections = {
    BubbleConchRoom: event.Collected("Open Bubble Conch Room"),
    SanctumEntryway: event.Collected("Disable Prismic Palace Seedragons"),
    SentryControlRoom: Any(
      event.Collected("Disable Prismic Palace Seedragons"),
      carrying.jester_boots,
      item.sprint | carrying.bubble_conch | carrying.shelnerts_fish
    )
  }

@lazy_region
def BubbleConchRoomHighShrooms(r: Region):
  r.locations = {
    "Shroom: Palace Interior - Bubble Conch Room 4": None,
    "Shroom: Palace Interior - Bubble Conch Room 5": None,
  }

  r.region_connections = {
    BubbleConchRoom: None
  }


@lazy_region
def BubbleConchRoom(r: Region):
  r.locations = {
    "Shroom: Palace Interior - Bubble Conch Room 1": None,
    "Shroom: Palace Interior - Bubble Conch Room 2": None,
    "Shroom: Palace Interior - Bubble Conch Room 3": None,

    "Palace Interior - Bubble Conch": None
  }

  r.region_connections = {
    BubbleConchRoomHighShrooms: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      carrying.bubble_conch,
      carrying.shelnerts_fish,
      item.sprint,
      item.double_jump,
      tech.ground_tail_jump,
      tech.air_tail_jump,
      item.wings,
      tech.bubble_jump,
      item.air_swim,
    ),
    Main: event.Collected("Open Bubble Conch Room")
  }

@lazy_region
def SanctumEntryway(r: Region):
  r.locations = {
    "Shroom: Palace Interior - Heaven's Path Entry 1": None,
    "Shroom: Palace Interior - Heaven's Path Entry 2": None,
    "Shroom: Palace Interior - Heaven's Path Entry 3": None
  }

  from . import Sanctum

  r.entrances = [
    SanctumDoor.define(Sanctum.PalaceDoor)
  ]

  r.region_connections = {
    Main: event.Collected("Disable Prismic Palace Seedragons")
  }

@lazy_region
def SentryControlRoom(r: Region):
  r.locations = {
    "Palace Interior - Sentry Control Preston": None,

    "Shroom: Palace Interior - Sentry Control Chamber 1": None,
    "Shroom: Palace Interior - Sentry Control Chamber 2": None,
    "Shroom: Palace Interior - Sentry Control Chamber 3": None,
  }

  r.region_connections = {
    Main: Any(
      event.Collected("Disable Prismic Palace Seedragons"),
      item.sprint | carrying.bubble_conch
    )
  }

@lazy_region
def Basement(r: Region):
  from . import Valley

  r.entrances = [
    BasementDoor.define(Valley.PalaceBasementDoor)
  ]

  r.region_connections = {
    BasementEggPlatform: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,

      event.Collected(KnockedPillarsDown) & Any(
        item.wings,
        tech.bubble_jump,
        tech.air_tail_jump,
        tech.ground_tail_jump,
        item.double_jump,
      ),

      tech.super_bubble_jump,
      item.double_jump & Any(
        item.wings,
        item.air_tail & item.roll,
        item.horn & tech.z_target & tech.bubble_jump_and_recoil,
        tech.bubble_jump & Any(
          tech.ground_tail_jump,
          tech.air_tail_jump,
        )
      ),
      tech.wing_jump & Any(
        tech.wing_storage,
        tech.bubble_jump_and_recoil & tech.z_target
      ),
      item.wings & Any(
        item.horn,
        tech.air_tail_jump,
        tech.ground_tail_jump,
      ),
      item.air_tail & item.roll,
    )
  }

@lazy_region
def BasementEggPlatform(r: Region):
  r.locations = {
    "Egg: Palace Interior - Basement": None
  }

  r.region_connections = {
    Basement: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,

      event.Collected(KnockedPillarsDown) & Any(
        tech.wing_jump,
        tech.air_tail_jump,
        tech.ground_tail_jump,
        item.double_jump,
      ),

      tech.super_bubble_jump,
      item.double_jump & Any(
        item.air_tail & item.roll,
        item.horn & tech.z_target & tech.bubble_jump_and_recoil,
        tech.bubble_jump & Any(
          tech.ground_tail_jump,
          tech.air_tail_jump,
        ),
        item.wings & Any(
          item.horn,
          tech.ability_toggle
        )
      )
    )
  }
