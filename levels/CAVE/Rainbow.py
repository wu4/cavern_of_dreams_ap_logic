from logic.comment import Comment
from ...logic import Any, Region, Entrance
from ...logic import item, tech, carrying, difficulty


class Main(Region): pass
class MoonLedges(Region): pass
class ShroomLedges(Region): pass
class Topside(Region): pass

class Well(Entrance): pass

from ..CAVE import GalleryLobby

regions = [
  Main.define(
    region_connections = {
      MoonLedges: Any(
        tech.any_super_jump,

        Comment(
          "Build height on the outside of the gate",
          carrying.jester_boots
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
      )
    },

    entrances = [
      Well.define(GalleryLobby.RainbowBench)
    ]
  ),

  MoonLedges.define(
    region_connections = {
      Main: None,

      ShroomLedges: Any(
        tech.any_super_jump,

        carrying.jester_boots,

        item.bubble,

        item.double_jump,

        item.air_tail & item.roll & difficulty.hard,

        item.horn & tech.momentum_cancel
      )
    }
  ),

  ShroomLedges.define(
    region_connections = {
      Main: None,

      Topside: Any(
        Comment(
          """Walk all of the way out of bounds to the green dragon, then
          carefully walk off to gain enough height for the final platform""",
          difficulty.hard & carrying.jester_boots
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
  ),

  Topside.define(
    region_connections = {
      Main: None
    },

    locations = {
      "Card: Dream": Any(
        tech.any_super_jump,

        item.high_jump,

        item.double_jump,

        item.air_tail & item.roll,

        item.horn
      )
    }
  )
]
