from ...logic import Entrance, Region, Any, All
from ...logic import tech, item, carrying, difficulty

class ArmadaLobbyDoor(Entrance): pass
class GalleryDoor(Entrance): pass

class ArmadaLobbySide(Region): pass
class GallerySide(Region): pass

from . import ArmadaLobby as _ArmadaLobby
from ..GALLERY import WaterLobby as _WaterLobby

regions = [
  ArmadaLobbySide.define(
    locations = {
      "Card: Sewer - Armada Lobby Side": None
    },

    entrances = [
      ArmadaLobbyDoor.define(_ArmadaLobby.SewerDoor)
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
      GalleryDoor.define(_WaterLobby.SewerDoor)
    ],

    region_connections = {
      ArmadaLobbySide: Any(
        Carrying("Jester Boots"),

        CanSuperJump,
        
        HasDoubleJump & (HasWings | CanTailJump()),

        Comment(
          "From the pipe: Hijump, instant hover + bubble float, turnaround (or z-target) bubble shots",
          (Difficulty("Intermediate") | Tech("z_target")) & HasHighJump & CanBubbleJump & CanHoverJump & CanHoverShoot
        ),

        CanTailJump(
          groundedExtraLogic = HasBubble | HasWings,
          aerialExtraLogic = HasWings | (HasBubble & HasHighJump)
        ),

        HasAirTail & HasRoll & HasSprint
      )
    }
  )
]
