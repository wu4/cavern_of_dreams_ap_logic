from ...logic import *

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
        CanSuperJump,

        HasDoubleJump & HasWings & (CanTailJump() | HasHorn),

        All(
          Carrying("Jester Boots"),
          HasDoubleJump | (Tech("tail_jump") & HasGroundTail)
        ),

        All(
          Difficulty("Hard"),
          Carrying("Jester Boots") & CanHoverShoot & CanHoverJump
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