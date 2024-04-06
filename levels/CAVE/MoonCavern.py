from ...logic import *

class Main(Region): pass
class DiveRoom(Region): pass
class DivePuzzleLedge(Region): pass
class UpperConnector(Region): pass
class Upper(Region): pass
class LavaMushroomPlatform(Region): pass
class DiveHoles(Region): pass
class NightmareLobbyDoorway(Region): pass

class SunCavernDoor(Entrance): pass
class PalaceLobbyDoor(Entrance): pass
class GalleryLobbyDoor(Entrance): pass

class DousedGalleryLobbyFlame(InternalEvent): pass
class SolvedDivePuzzle(InternalEvent): pass

from . import SunCavern as _SunCavern
from . import PalaceLobby as _PalaceLobby
from . import GalleryLobby as _GalleryLobby

regions = [
  Main.define(
    locations = {
      "Card: Moon Cavern - Dive": HasSwim & Whackable(horn_works = True),
      
      "Shroom: Moon Cavern - Lava Platforms 1": None,
      "Shroom: Moon Cavern - Lava Platforms 2": None,
      "Shroom: Moon Cavern - Lava Platforms 3": None,
      "Shroom: Moon Cavern - Lava Platforms 4": None,

      "Shroom: Moon Cavern - Potionfall": None,
      
      SolvedDivePuzzle: HasHorn
    },

    entrances = [
      SunCavernDoor.define(
        _SunCavern.MoonCavernHeartDoor
      )
    ],

    region_connections = {
      DiveHoles: Whackable(horn_works = True),

      DiveRoom: Any(
        Whackable(horn_works = True),

        Comment(
          "Vine entrance",
          Whackable(air_tail_works = True, throwable_works = True)
        )
      ),

      DivePuzzleLedge: Any(
        HasHorn,

        CanSuperJump,
        Carrying("Jester Boots"),
        
        Comment(
          "Extinguish the Keehee and use him as a platform",
          Carrying("Potion") | HasBubble
        ),

        HasDoubleJump & CanTailJump(),

        HasWings & Any(
          HasDoubleJump,
          All(
            Tech("tail_jump") & HasGroundTail,
            Tech("hover_jump") | HasHighJump
          )
        )
      ),

      UpperConnector: Any(
        CanSuperJump,
        HighJumpObstacle,

        Comment(
          "Bouncy mushroom + Keehee damage boost",
          CanDamageBoost()
        ),

        Comment(
          "Bouncy mushroom + Z-target bubble shooting",
          Tech("z_target") & CanBubbleJump
        ),

        Comment(
          "Hover from bouncy shroom",
          HasWings
        )
      ),

      Upper: Any(
        CanSuperJump,
        
        Comment(
          "Hover from bouncy shroom",
          HasWings
        ),

        Comment(
          "Bouncy mushroom + Keehee damage  boost while bubble floating",
          CanDamageBoost(CanBubbleJump)
        )
      ),

      LavaMushroomPlatform: None
    }
  ),
  
  DiveHoles.define(
    locations = {
      "Shroom: Moon Cavern - Dive Holes 1": None,
      "Shroom: Moon Cavern - Dive Holes 2": None,
      "Shroom: Moon Cavern - Dive Holes 3": None,
      "Shroom: Moon Cavern - Dive Holes 4": None,
      "Shroom: Moon Cavern - Dive Holes 5": None,
      "Shroom: Moon Cavern - Dive Holes 6": None,
    },

    region_connections = {
      Main: None
    }
  ),

  UpperConnector.define(
    locations = {
      "Shroom: Moon Cavern - Lonely Shroom": None
    },

    region_connections = {
      Main: None,
      
      Upper: HighJumpObstacle
    }
  ),

  Upper.define(
    locations = {
      "Egg: Moon Cavern - Keehee Climb": Any(
        CanSuperJump,
        Carrying("Jester Boots"),

        HasClimb & HasWings & (HasHighJump | HasHorn),
      ),

      "Card: Moon Cavern - Statue": None,

      "Shroom: Moon Cavern - Palace Lobby Entryway 1": None,
      "Shroom: Moon Cavern - Palace Lobby Entryway 2": None,
      "Shroom: Moon Cavern - Palace Lobby Entryway 3": None,
      "Shroom: Moon Cavern - Palace Lobby Pathway 1": None,
      "Shroom: Moon Cavern - Palace Lobby Pathway 2": None,
      "Shroom: Moon Cavern - Palace Lobby Pathway 3": None,
      "Shroom: Moon Cavern - Palace Lobby Statue 1": None,
      "Shroom: Moon Cavern - Palace Lobby Statue 2": None,
    },

    entrances = [
      PalaceLobbyDoor.define(
        _PalaceLobby.MoonCavernDoor
      )
    ],

    region_connections = {
      UpperConnector: None
    }
  ),

  LavaMushroomPlatform.define(
    locations = {
      "Shroom: Moon Cavern - Lava Mushroom Platform 1": None,
      "Shroom: Moon Cavern - Lava Mushroom Platform 2": None
    },

    region_connections = {
      NightmareLobbyDoorway: None,

      Main: Any(
        HighJumpObstacle,

        Comment(
          "Boost off of the Keehee to the Dive Holes side",
          CanDamageBoost(
            Difficulty("Hard") | CanBubbleJump
          )
        )
      )
    }
  ),

  NightmareLobbyDoorway.define(
    locations = {
      DousedGalleryLobbyFlame: Carrying("Potion") | HasBubble
    },

    entrances = [
      GalleryLobbyDoor.define(
        _GalleryLobby.MoonCavernDoor,
        Any(
          Has(DousedGalleryLobbyFlame),
          CanDamageBoost(Difficulty("Hard") & Tech("momentum_cancel"))
        )
      )
    ],

    region_connections = {
      LavaMushroomPlatform: None
    }
  ),

  DiveRoom.define(
    locations = {
      "Egg: Moon Cavern - Dive Puzzle": Has(SolvedDivePuzzle)
    },

    region_connections = {
      Main: HasClimb
    }
  )
]