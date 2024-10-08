from ...logic.comment import Comment
from ...logic import lazy_region, Region, Any, Entrance
from ...logic import item, tech, carrying, difficulty

area_path = "CAVE/Rainbow"

class WellEntrance(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromRainbowToGalleryLobby"
  dest_path = f"{area_path}/Warps/DestFromGalleryLobbyToRainbow"

@lazy_region
def Main(r: Region):
  r.region_connections = {
    MoonLedges: Any(
      tech.any_super_jump,

      Comment(
        "Build height on the outside of the gate",
        tech.jester_boots_slope_movement
      ),

      Comment(
        "Conk on the geometry next to the ledge to short hop, then hijump",
        item.high_jump
      ),

      item.horn,

      Comment(
        "Jump from the well",
        tech.ground_tail_jump & item.double_jump,
      ),
    ),

    Well: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      tech.bubble_jump,
      item.double_jump,
      tech.air_tail_jump,
      tech.ground_tail_jump,
      item.sprint & item.roll,
      tech.momentum_cancel & item.high_jump
    )
  }

@lazy_region
def MoonLedges(r: Region):
  r.region_connections = {
    Main: None,

    Well: None,

    ShroomLedges: Any(
      tech.any_super_jump,

      carrying.jester_boots,

      carrying.mr_kerringtons_wings & Any(
        # this is technically performable without any bonus items
        # but it becomes a lot more consistent with them
        # losing a temporary item after 1 failed attempt would kinda suck
        item.sprint,
        tech.momentum_cancel & item.high_jump,
        item.double_jump
      ),

      item.bubble,

      item.double_jump,

      item.air_tail & item.roll & difficulty.hard,

      item.horn & Any(
        item.wings,
        tech.momentum_cancel
      )
    )
  }

@lazy_region
def ShroomLedges(r: Region):
  r.region_connections = {
    Main: None,

    Topside: Any(
      Comment(
        """Walk all of the way out of bounds to the green dragon, then
        carefully walk off to gain enough height for the final platform""",
        difficulty.hard & tech.out_of_bounds & tech.jester_boots_slope_movement
      ),

      item.horn,

      Comment(
        "Double jump after conking on the ceiling from the bouncy shroom",
        item.double_jump
      ),

      item.high_jump & item.double_jump & tech.momentum_cancel,

      Comment(
        "Speedy roll, then jump into the bouncy shroom",
        item.air_tail & item.roll,
      ),

      tech.z_target & tech.bubble_jump
    )
  }

@lazy_region
def Topside(r: Region):
  r.locations = {
    "Card: Dream": Any(
      tech.any_super_jump,

      item.high_jump,

      item.double_jump,

      item.air_tail & item.roll,

      item.horn
    )
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def Well(r: Region):
  from . import GalleryLobby

  r.region_connections = {
    Main: None
  }

  r.entrances = [
    WellEntrance.define(
      default_connection = GalleryLobby.RainbowBench,
    )
  ]
