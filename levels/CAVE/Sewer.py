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
      ArmadaLobbyDoor.define(
        default_connection = ArmadaLobby.SewerDoor
      )
    ],

    region_connections = {
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

        carrying.jester_boots & Any(
          difficulty.intermediate & (item.double_jump | tech.ground_tail_jump),
          item.double_jump & tech.ground_tail_jump
        ),

        Comment(
          "Shoot to bounce upwards from the top of the pipe and carry wing storage to the bars",
          All(
            difficulty.hard,
            carrying.jester_boots,
            tech.wing_storage,
            tech.bubble_jump_and_recoil
          )
        )
      )
    }
  ),

  GallerySide.define(
    locations = {
      "Card: Sewer - Gallery of Nightmares Side": None
    },

    entrances = [
      GalleryDoor.define(
        default_connection = WaterLobby.SewerDoor
      )
    ],

    region_connections = {
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
  )
]
