from ...logic import lazy_region, Region, Entrance, Any, All
from ...logic import tech, item, carrying, difficulty
from ...logic.comment import Comment

area_path = "CAVE/Sewer"

class ArmadaLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromSewerToMonsterLobby"
  dest_path = f"{area_path}/Warps/DestFromMonsterLobbyToSewer"
class GalleryDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromSewerToWaterLobby"
  dest_path = f"{area_path}/Warps/DestFromWaterLobbyToSewer"

@lazy_region
def ArmadaLobbySide(r: Region):
  r.locations = {
    "Card: Sewer - Armada Lobby Side": None
  }

  from . import ArmadaLobby

  r.entrances = [
    ArmadaLobbyDoor.define(
      default_connection = ArmadaLobby.SewerDoor
    )
  ]

  r.region_connections = {
    GallerySide: Any(
      tech.any_super_jump,

      item.double_jump & Any(
        tech.wing_storage,

        tech.ability_toggle & Any(
          carrying.mr_kerringtons_wings,
          carrying.jester_boots & item.wings
        ),

        item.wings & (tech.air_tail_jump | tech.ground_tail_jump | item.horn),
      ),

      tech.jester_boots_slope_movement & Any(
        difficulty.intermediate & (item.double_jump | tech.ground_tail_jump),
        item.double_jump & tech.ground_tail_jump
      ),

      Comment(
        """
        Shoot to bounce upwards from the slope of the pipe, gaining height with
        the jester boots, and carry wing storage to the bars
        """,
        difficulty.hard &
          tech.jester_boots_slope_movement &
          tech.wing_storage &
          tech.bubble_jump_and_recoil
      )
    )
  }

@lazy_region
def GallerySide(r: Region):
  r.locations = {
    "Card: Sewer - Gallery of Nightmares Side": None
  }

  from ..GALLERY import WaterLobby

  r.entrances = [
    GalleryDoor.define(
      default_connection = WaterLobby.SewerDoor
    )
  ]

  r.region_connections = {
    ArmadaLobbySide: Any(
      carrying.jester_boots,
      tech.any_super_jump,
      tech.wing_storage,
      carrying.mr_kerringtons_wings,

      item.double_jump & Any(
        item.wings,
        tech.ground_tail_jump,
        tech.air_tail_jump
      ),

      Comment(
        """
        From the pipe: Hijump, instant hover + bubble float, turnaround (or
        z-target) bubble shots
        """,
        All(
          difficulty.intermediate | tech.z_target,
          item.high_jump,
          tech.bubble_jump_and_recoil,
          tech.wing_jump
        )
      ),

      Comment(
        "Dive into the bouncy shroom",
        item.horn & Any(
          item.sprint,
          item.wings,
          item.double_jump,
          tech.bubble_jump,
          Comment(
            """
            Bounce with air tail, then immediately double-tap the tail button
            to dive as soon as possible
            """,
            difficulty.hard & item.air_tail
          ),
          Comment(
            """
            Jump with ground tail, then immediately dive
            """,
            difficulty.intermediate & item.ground_tail
          )
        ),
      ),

      tech.ground_tail_jump & Any(
        tech.bubble_jump,
        item.wings
      ),

      tech.air_tail_jump & Any(
        item.wings,
        item.bubble & item.high_jump
      ),

      item.air_tail & item.roll & item.sprint
    )
  }
