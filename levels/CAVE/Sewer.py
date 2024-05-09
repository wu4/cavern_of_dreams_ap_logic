from ...logic import Entrance, Region, Any, All
from ...logic.comment import Comment
from ...logic import tech, item, carrying, difficulty

armada_lobby_door = Entrance("Armada Lobby Door")
gallery_door = Entrance("Gallery Door")

from . import ArmadaLobby
from ..GALLERY import WaterLobby

armada_lobby_side = Region("Armada Lobby Side")
gallery_side = Region ("Gallery Side")

regions = [
  armada_lobby_side.define(
    locations = {
      "Card: Sewer - Armada Lobby Side": None
    },

    entrances = [
      armada_lobby_door.define(ArmadaLobby.sewer_door)
    ],

    region_connections = {
      gallery_side: Any(
        tech.any_super_jump,

        item.double_jump & item.wings & (tech.air_tail_jump | tech.ground_tail_jump | item.horn),

        All(
          carrying.jester_boots,
          item.double_jump | tech.ground_tail_jump
        ),

        All(
          difficulty.hard,
          carrying.jester_boots & tech.hover_jump & tech.hover_shoot
        )
      )
    }
  ),

  gallery_side.define(
    locations = {
      "Card: Sewer - Gallery of Nightmares Side": None
    },

    entrances = [
      gallery_door.define(WaterLobby.sewer_door)
    ],

    region_connections = {
      armada_lobby_side: Any(
        carrying.jester_boots,

        tech.any_super_jump,
        
        item.double_jump & (item.wings | tech.ground_tail_jump | tech.air_tail_jump),

        Comment(
          "From the pipe: Hijump, instant hover + bubble float, turnaround (or z-target) bubble shots",
          All(
            difficulty.intermediate | tech.z_target,
            item.high_jump,
            tech.bubble_jump,
            tech.hover_jump,
            tech.hover_shoot
          )
        ),

        tech.ground_tail_jump & (item.bubble | item.wings),
        tech.air_tail_jump & (item.wings | (item.bubble & item.high_jump)),

        item.air_tail & item.roll & item.sprint
      )
    }
  )
]
