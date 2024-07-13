from ...logic import lazy_region, Region, Entrance, InternalEvent, Any
from ...logic import item, carrying, tech, event, difficulty

area_path = "CHALICE/Chalice (Main)"

class FireLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromChaliceToGallery"
  dest_path = f"{area_path}/Warps/DestPaintingChalice"

class ShortcutDownDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpChaliceShortcut"
  dest_path = f"{area_path}/Warps/DestChaliceShortcutReverse"

class ShortcutUpDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpChaliceShortcutReverse"
  dest_path = f"{area_path}/Warps/DestChaliceShortcut"

class OpenedLowerSnake(InternalEvent): pass

@lazy_region
def Main(r: Region):
  from . import FireLobby

  r.entrances = [
    FireLobbyDoor.define(FireLobby.ChalicePainting),
    ShortcutDownDoor.define(
      default_connection = ShortcutUpDoor,
      rule = event.Collected("Coils of Agony - Open Shortcut")
    )
  ]

  r.region_connections = {
    EggPlatform: Any(
      event.Collected("Coils of Agony - Open Shortcut"),
      tech.any_super_jump,
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
      tech.bubble_jump & Any(
        item.horn,
        item.double_jump,
      ),
      item.wings & Any(
        item.high_jump,
        item.double_jump,
        item.horn
      ),
      item.air_tail & item.roll,
      Any(
        tech.air_tail_jump & item.high_jump,
        tech.ground_tail_jump
      ) & Any(
        tech.bubble_jump,
        item.double_jump,
        item.wings,
        difficulty.intermediate
      )
    ),

    BottomShortcutPlatform: event.Collected(OpenedLowerSnake)
  }

@lazy_region
def EggPlatform(r: Region):
  r.locations = {
    "Egg: Coils of Agony": None
  }

  r.region_connections = {
    Main: Any(
      event.Collected("Coils of Agony - Open Shortcut"),
      tech.any_super_jump,
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
      carrying.no_temp_items,
      item.wings,
      tech.bubble_jump,
      item.double_jump,
      item.air_tail & item.roll,
      tech.ground_tail_jump,
      tech.air_tail_jump,
    )
  }

@lazy_region
def BottomShortcutPlatform(r: Region):
  r.locations = {
    OpenedLowerSnake: None
  }

  r.entrances = [
    ShortcutUpDoor.define(
      default_connection = ShortcutDownDoor,
      rule = event.Collected("Coils of Agony - Open Shortcut")
    )
  ]

  r.region_connections = {
    Main: None
  }
