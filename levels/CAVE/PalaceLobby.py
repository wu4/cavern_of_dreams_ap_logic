from ...logic import lazy_region, Region, Entrance, Any
from ...logic import item, tech, carrying
from ...logic.comment import Comment
from ...logic import event
from ...logic import difficulty

area_path = "CAVE/Palace Lobby"

class ValleyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromPalaceLobbyToPalace"
  dest_path = f"{area_path}/Warps/DestFromPalaceToPalaceLobby"
class MoonCavernDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromPalaceLobbyToDepths"
  dest_path = f"{area_path}/Warps/DestFromDepthsToPalaceLobby"
class SunCavernTeleport(Entrance):
  warp_path = f"{area_path}/Warps/Portal"
  dest_path = f"{warp_path}/DestFromPortal???"

@lazy_region
def Main(r: Region):
  from . import MoonCavern

  r.entrances = [
    MoonCavernDoor.define(MoonCavern.PalaceLobbyDoor)
  ]

  r.region_connections = {
    Underwater: item.swim,

    Ledges: Any(
      carrying.jester_boots,
      tech.any_super_jump,

      carrying.mr_kerringtons_wings & Any(
        tech.bubble_jump_and_recoil & tech.z_target,
        tech.wing_storage
      ),

      Comment(
        "Hijump double-jump followed by hover",
        tech.ground_tail_jump & item.high_jump & tech.wing_jump
      ),

      item.double_jump & item.wings,

      Comment(
        "Egg iceberg works as a platform",
        event.Collected("Activate Palace Lobby Whirlpool")
      )
    ),

    TopLedge: Any(
      event.Collected("Run Palace Lobby Faucet"),
    )
  }

@lazy_region
def Underwater(r: Region):
  r.locations = {
    "Shroom: Palace Lobby - Underwater 1": None,
    "Shroom: Palace Lobby - Underwater 2": None,
    "Shroom: Palace Lobby - Underwater 3": None,
    "Shroom: Palace Lobby - Underwater 4": None,
    "Shroom: Palace Lobby - Underwater 5": None,
    "Shroom: Palace Lobby - Underwater 6": None,

    "Palace Lobby Whirlpool Preston": None,

    "Egg: Palace Lobby - Submerged": None,
  }

  r.region_connections = {
    Main: None,

    PrismicEntryPlatform: Any(
      item.sprint,

      item.air_swim,

      carrying.shelnerts_fish | carrying.bubble_conch
    ),

    TopLedge: Any(
      item.air_swim,

      carrying.shelnerts_fish | carrying.bubble_conch
    )
  }

@lazy_region
def Ledges(r: Region):
  r.locations = {
    "Shroom: Palace Lobby - Ledges 1": None,
    "Shroom: Palace Lobby - Ledges 2": None,
    "Shroom: Palace Lobby - Ledges 3": None,
    "Shroom: Palace Lobby - Ledges 4": None,
    "Shroom: Palace Lobby - Ledges 5": None,
    "Shroom: Palace Lobby - Ledges 6": None
  }

  r.region_connections = {
    Main: Any(
      item.wings,
      item.roll & item.air_tail,
      tech.bubble_jump & Any(
        item.high_jump,
        item.sprint,
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump
      )
    ),

    PrismicEntryPlatform: Any(
      event.Collected("Run Palace Lobby Faucet"),

      item.wings & Any(
        item.double_jump,
        item.horn
      ),

      Comment(
        "High + Wing jump from slanted platform to stationary iceberg",
        tech.wing_jump & item.high_jump
      ),

      event.Collected("Activate Palace Lobby Whirlpool") & Any(
        Comment(
          "Precise horn jump from extended ledge onto the tall iceberg. Dive late in the jump arc to gain some extra distance",
          difficulty.hard & item.horn
        ),

        item.air_tail,
        item.ground_tail,

        Comment(
          "Ejection launch from egg iceberg onto tall iceberg as they clip together",
          tech.ejection_launch
        )
      )
    )
  }

@lazy_region
def PrismicEntryPlatform(r: Region):
  r.locations = {
    "Palace Lobby Faucet Preston": None
  }

  from ..PALACE import Valley
  from . import SunCavern

  r.entrances = [
    ValleyDoor.define(
      default_connection = Valley.PalaceLobbyDoor
    ),
    SunCavernTeleport.define(
      default_connection = SunCavern.PalaceLobbyTeleport,
      rule = event.Collected("Open Palace Lobby Teleport") & carrying.no_jester_boots
    )
  ]

  r.region_connections = {
    Ledges: Any(
      event.Collected("Activate Palace Lobby Whirlpool"),
      carrying.mr_kerringtons_wings,

      item.wings,

      tech.bubble_jump & Any(
        item.sprint,
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump
      ),

      Comment(
        "Hijump bubble shot float from the stationary iceberg",
        tech.bubble_jump_and_recoil & item.high_jump
      ),

      item.air_tail & item.roll
    ),

    TopLedge: Any(
      item.horn & item.double_jump,

      carrying.mr_kerringtons_wings & Any(
        tech.wing_storage,
        item.high_jump,
        item.double_jump
      ),

      item.double_jump & item.high_jump & Any(
        tech.ground_tail_jump,

        item.wings
      ),

      tech.bubble_jump_and_recoil & tech.wing_jump & Any(
        tech.ground_tail_jump,

        item.double_jump,
        item.high_jump,
        item.horn,
      )
    )
  }

@lazy_region
def TopLedge(r: Region):
  r.locations = {
    "Card: Palace Lobby - Top": None
  }

  r.region_connections = {
    Main: None,
    PrismicEntryPlatform: None,
    Ledges: None
  }
