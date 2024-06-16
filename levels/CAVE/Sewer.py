from ...logic import Entrance, Region, Any, All
from ...logic import tech, item, carrying, difficulty
from ...logic.comment import Comment

class ArmadaLobbyDoor(Entrance): pass
class GalleryDoor(Entrance): pass

class ArmadaLobbySide(Region): pass
class GallerySide(Region): pass

from . import ArmadaLobby
from ..GALLERY import WaterLobby

regions = [
  ArmadaLobbySide.define(
    locations = {
      "Card: Sewer - Armada Lobby Side": None
    },

    entrances = [
      ArmadaLobbyDoor.define(ArmadaLobby.SewerDoor)
    ],

    region_connections = {
      GallerySide: Any(
        tech.any_super_jump,

        item.double_jump & item.wings & (tech.air_tail_jump | tech.ground_tail_jump | item.horn),

        carrying.jester_boots & Any(
          item.double_jump,
          tech.ground_tail_jump
        ),

        All(
          difficulty.hard,
          carrying.jester_boots & tech.bubble_jump_and_recoil & tech.wing_jump
        )
      )
    }
  ),

  GallerySide.define(
    locations = {
      "Card: Sewer - Gallery of Nightmares Side": None
    },

    entrances = [
      GalleryDoor.define(WaterLobby.SewerDoor)
    ],

    region_connections = {
      ArmadaLobbySide: Any(
        carrying.jester_boots,
        tech.any_super_jump,

        item.double_jump & Any(
          item.wings,
          tech.ground_tail_jump,
          tech.air_tail_jump
        ),

        Comment(
          "From the pipe: Hijump, instant hover + bubble float, turnaround (or z-target) bubble shots",
          (difficulty.intermediate | tech.z_target) & item.high_jump & tech.bubble_jump_and_recoil & tech.wing_jump
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
  )
]
