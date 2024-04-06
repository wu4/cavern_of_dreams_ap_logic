from ...logic import *

class Main(Region): pass
class ArmadaLobbyRoom(Region): pass
class HighJumpLedge(Region): pass
class VineLedge(Region): pass
class TailSpinLedge(Region): pass
class MightyWallLedge(Region): pass
class WaterfallLedge(Region): pass
class DucklingsLedge(Region): pass
class DucklingsDoorway(Region): pass
class MoonCavernHeartDoorway(Region): pass

class LostleafLobbyDoor(Entrance): pass
class DucklingsDoorUpper(Entrance): pass
class DucklingsDoorLower(Entrance): pass
class MoonCavernHeartDoor(Entrance): pass
class ArmadaLobbyDoor(Entrance): pass
class LostleafLobbyTeleport(Entrance): pass
class ArmadaLobbyTeleport(Entrance): pass
class PalaceLobbyTeleport(Entrance): pass
class GalleryLobbyTeleport(Entrance): pass

class MoonCavernHeartDoorOpened(InternalEvent): pass

from . import LostleafLobby as _LostleafLobby
from . import ArmadaLobby as _ArmadaLobby
from . import PalaceLobby as _PalaceLobby
from . import GalleryLobby as _GalleryLobby
from ..LAKE import LostleafLake as _LostleafLake
from . import MoonCavern as _MoonCavern

regions = [
  Main.define(
    locations = {
      "Sun Cavern - Sage's Blessing 1": HasEggs(1),
      "Sun Cavern - Sage's Blessing 2": HasEggs(6),
      "Sun Cavern - Sage's Blessing 3": HasEggs(12),
      "Sun Cavern - Sage's Blessing 4": HasEggs(24),
      "Sun Cavern - Sage's Blessing 5": HasEggs(40),

      "Card: Sun Cavern - Air Vent": None,

      "Shroom: Sun Cavern - Mighty Wall Ground 1": None,
      "Shroom: Sun Cavern - Mighty Wall Ground 2": None,
      "Shroom: Sun Cavern - Mighty Wall Ground 3": None,
      "Shroom: Sun Cavern - Mighty Wall Ground 4": None,

      "Fed Lostleaf Lake Fella":         HasShrooms("Lake")    & (HasGroundTail | HasAirTail),
      "Fed Airborne Armada Fella":       HasShrooms("Monster") & (HasGroundTail | HasAirTail),
      "Fed Prismic Palace Fella":        HasShrooms("Palace")  & (HasGroundTail | HasAirTail),
      "Fed Gallery of Nightmares Fella": HasShrooms("Gallery") & (HasGroundTail | HasAirTail),
    },
    
    entrances = [
      LostleafLobbyTeleport.define(
        to = _LostleafLobby.SunCavernTeleport,
        rule = Has("Open Lake Lobby Teleport")
      ),

      ArmadaLobbyTeleport.define(
        to = _ArmadaLobby.SunCavernTeleport,
        rule = Has("Open Armada Lobby Teleport")
      ),

      PalaceLobbyTeleport.define(
        to = _PalaceLobby.SunCavernTeleport,
        rule = Has("Open Palace Lobby Teleport")
      ),

      GalleryLobbyTeleport.define(
        to = _GalleryLobby.SunCavernTeleport,
        rule = Has("Open Gallery Lobby Teleport")
      ),
    ],

    region_connections = {
      ArmadaLobbyRoom: Any(
        HasHorn,
        HasWings,

        Carrying("Jester Boots"),
        CanSuperJump,
        
        Comment(
          "Well-spaced high jump into the fan",
          HasHighJump & (HasSprint | CanBubbleJump)
        )
      ),

      HighJumpLedge: Any(
        HasHighJump,
        HasDoubleJump,

        Carrying("Jester Boots"),
        CanSuperJump,
        
        Comment(
          "Hover-jump into the nearby tutorial stone",
          CanHoverJump
        ),

        Comment(
          "Hover-shoot into the nearby tutorial stone",
          CanHoverShoot
        ),

        Comment(
          "Build speed and roll into the nearby tutorial stone",
          HasSprint & HasRoll
        )
      ),
      
      VineLedge: Any(
        HasClimb,
        CanSuperJump,
        
        Comment(
          "Hover-jump up the sun wall",
          CanHoverJump
        ),
        
        Comment(
          "Climb the nearby stalagmite or sun wall with hover + bubble shots",
          CanHoverShoot
        ),
        
        Comment(
          "Tail jump double jump from the nearby tutorial stone",
          HasDoubleJump & CanTailJump(
            groundedExtraLogic = HasHighJump | HasWings,
            aerialExtraLogic = HasHighJump & HasWings
          )
        )
      ),
      
      TailSpinLedge: Any(
        Carrying("Jester Boots"),
        CanSuperJump,

        Comment(
          "Roll jump makes the distance",
          HasRoll
        ),
        
        HasHighJump,
        
        HasBubble,

        HasWings,
        
        CanTailJump()
      ),

      MightyWallLedge: Any(
        HasClimb,
        Carrying("Jester Boots"),
        CanSuperJump,

        Comment(
          "Dive-bounce off of shroom",
          HasHorn
        ),

        Comment(
          "Jump up a tutorial stone and spire to reach the egg ledge",
          Any(
            HasDoubleJump & (HasHighJump | HasWings),

            All(
              Difficulty("Intermediate"),
              CanTailJump(
                groundedExtraLogic = None,
                aerialExtraLogic = HasHighJump | HasDoubleJump
              )
            )
          )
        ),
      ),

      WaterfallLedge: Any(
        Carrying("Jester Boots"),
        CanSuperJump,

        Comment(
          "Very high jump from one of the nearby gems",
          All (
            Difficulty("Intermediate"),
            Tech("tail_jump"),
            HasGroundTail & HasHighJump & HasDoubleJump & HasWings
          )
        )
      ),
      

      DucklingsLedge: Any(
        HasHorn,
        HasWings,
        HasDoubleJump,
        CanSuperJump,

        HasRoll & (HasSprint | HasAirTail),

        CanTailJump(
          groundedExtraLogic = None,
          aerialExtraLogic = Any(
            Comment(
              "Tail Spin from the right gem to the tiny leaf, then to the big leaf",
              Difficulty("Intermediate")
            ),
            HasHighJump
          )
        ),
      ),
      
      DucklingsDoorway: Any(
        CanSuperJump,
        
        Comment(
          "Float to the big leaf from the Sage ramp",
          HasSprint & (CanHoverJump | CanBubbleJump)
        ),
        
        Comment(
          "Jump to the small leaf from the right crystal",
          Difficulty("Intermediate") & Tech("tail_jump") & HasAirTail
        ),

        Comment(
          "Speedy launch from the Sage ramp",
          HasSprint & HasRoll & HasAirTail
        ),
        
        Comment(
          "Hover shoot from the Sage ramp",
          CanHoverShoot
        ),
        
        Comment(
          "Precise use of bubble float and shoot jumping to land on the leaf from the right gem",
          Difficulty("Intermediate") & CanBubbleJump
        ),
        
        Tech("momentum_cancel") & HasWings,

        Comment(
          "Clever use of wings and riding up the left gem's geometry to jump on a leaf",
          Difficulty("Intermediate") & CanHoverJump
        )
      ),

      MoonCavernHeartDoorway:
        HasSwim & Any(
          HasHorn,
          HasSprint,
          Difficulty("Intermediate"),
        )
    },
  ),

  ArmadaLobbyRoom.define(
    locations = {
      "Shroom: Sun Cavern - Armada Entrance 1" : None,
      "Shroom: Sun Cavern - Armada Entrance 2" : None,
      "Shroom: Sun Cavern - Armada Entrance 3" : None,
    },
    
    entrances = [
      ArmadaLobbyDoor.define(
        to = _ArmadaLobby.SunCavernDoor
      )
    ],

    region_connections = {
      Main: None
    }
  ),

  HighJumpLedge.define(
    locations = {
      "Shroom: Sun Cavern - High Jump Ledge 1": None,
      "Shroom: Sun Cavern - High Jump Ledge 2": None
    },
    region_connections = {
      Main: None
    }
  ),

  VineLedge.define(
    locations = {
      "Shroom: Sun Cavern - Vine Ledge 1": None,
      "Shroom: Sun Cavern - Vine Ledge 2": None
    },

    region_connections = {
      Main: None,
      HighJumpLedge: Any(
        CanHoverJump,
        HasRoll & (HasSprint | HasAirTail)
      )
    }
  ),

  TailSpinLedge.define(
    locations = {
      "Shroom: Sun Cavern - Tail Spin Ledge 1": None,
      "Shroom: Sun Cavern - Tail Spin Ledge 2": None
    },
      
    region_connections = {
      Main: None
    }
  ),

  MightyWallLedge.define(
    locations = {
      "Whack Mighty Wall": Any(
        HasAirTail,
        HasGroundTail,
        Carrying("Apple"),
        Carrying("Bubble Conch")
      ),

      "Egg: Sun Cavern - Mighty Wall": None,

      "Shroom: Sun Cavern - Mighty Wall Egg Ledge 1": None,
      "Shroom: Sun Cavern - Mighty Wall Egg Ledge 2": None,
      "Shroom: Sun Cavern - Mighty Wall Egg Ledge 3": None
    },

    entrances = [
      LostleafLobbyDoor.define(
        to = _LostleafLobby.SunCavernDoor,
        rule = Has("Topple Mighty Wall")
      )
    ],

    region_connections = {
      Main: None
    }
  ),

  WaterfallLedge.define(
    locations = {
      "Egg: Sun Cavern - Waterfall": None
    },

    entrances = [
      DucklingsDoorUpper.define(
        to = _LostleafLake.DucklingsDoorUpper
      )
    ],

    region_connections = {
      Main: None,
      
      DucklingsDoorway: Comment(
        "Simply float down",
        CanBubbleJump | CanHoverJump
      ),

      MoonCavernHeartDoorway: Comment(
        "Jumping down lets you get past the jets",
        HasSwim
      )
    }
  ),

  DucklingsLedge.define(
    locations = {
      "Shroom: Sun Cavern - Ducklings Ledge 1": None,
      "Shroom: Sun Cavern - Ducklings Ledge 2": None
    },

    region_connections = {
      Main: None,
      DucklingsDoorway: HighJumpObstacle | CanSuperJump
    }
  ),
  
  DucklingsDoorway.define(
    entrances = [
      DucklingsDoorLower.define(
        to = _LostleafLake.DucklingsDoorLower
      )
    ],

    region_connections = {
      DucklingsLedge: None
    }
  ),

  MoonCavernHeartDoorway.define(
    entrances = [
      MoonCavernHeartDoor.define(
        to = _MoonCavern.SunCavernDoor,
        rule = Has(MoonCavernHeartDoorOpened)
      ),
    ],

    locations = {
      MoonCavernHeartDoorOpened:
        HasHearts(1) & Whackable(ground_tail_works = True, air_tail_works = True)
    },

    region_connections = {
      Main: HasSwim,

      DucklingsDoorway: 
        Comment(
          "Speedy launch from the waterjet",
          HasSwim
        )
    }
  )
]