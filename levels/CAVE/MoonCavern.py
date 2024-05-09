from ...logic import Any, All
from ...logic.objects import Region, Entrance, InternalEvent

from ...logic import item, event, difficulty, carrying, tech, templates
from ...logic.whackable import Whackable
from ...logic.comment import Comment

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
      "Card: Moon Cavern - Dive": item.Swim & Whackable(horn_works = True),
      
      "Shroom: Moon Cavern - Lava Platforms 1": None,
      "Shroom: Moon Cavern - Lava Platforms 2": None,
      "Shroom: Moon Cavern - Lava Platforms 3": None,
      "Shroom: Moon Cavern - Lava Platforms 4": None,

      "Shroom: Moon Cavern - Potionfall": None,
      
      SolvedDivePuzzle: item.Horn
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
        tech.AnySuperJump,
        carrying.JesterBoots,

        item.Horn,
        
        Comment(
          "Extinguish the Keehee and use him as a platform",
          carrying.Potion | item.Bubble
        ),

        item.DoubleJump & (tech.GroundTailJump | tech.AirTailJump),

        item.Wings & Any(
          item.DoubleJump,
          All(
            tech.GroundTailJump,
            tech.HoverJump & item.HighJump
          )
        )
      ),

      UpperConnector: Any(
        templates.HighJumpObstacle,

        Comment(
          "Bouncy mushroom + Keehee damage boost",
          tech.DamageBoost
        ),

        Comment(
          "Bouncy mushroom + Z-target bubble shooting",
          tech.ZTarget & tech.BubbleJump
        ),

        Comment(
          "Hover from bouncy shroom",
          item.Wings
        )
      ),

      Upper: Any(
        tech.AnySuperJump,
        
        Comment(
          "Hover from bouncy shroom",
          item.Wings
        ),

        Comment(
          "Bouncy mushroom + Keehee damage boost while bubble floating",
          tech.DamageBoost & tech.BubbleJump
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
      
      Upper: templates.HighJumpObstacle
    }
  ),

  Upper.define(
    locations = {
      "Egg: Moon Cavern - Keehee Climb": Any(
        tech.AnySuperJump,
        carrying.JesterBoots,

        item.Climb & item.Wings & (item.HighJump | item.Horn),
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
        templates.HighJumpObstacle,

        Comment(
          "Boost off of the Keehee to the Dive Holes side",
          tech.DamageBoost & (difficulty.Hard | tech.BubbleJump)
        )
      )
    }
  ),

  NightmareLobbyDoorway.define(
    locations = {
      DousedGalleryLobbyFlame: carrying.Potion | item.Bubble
    },

    entrances = [
      GalleryLobbyDoor.define(
        _GalleryLobby.MoonCavernDoor,
        Any(
          event.Collected(DousedGalleryLobbyFlame),
          difficulty.Hard & tech.DamageBoost & tech.MomentumCancel
        )
      )
    ],

    region_connections = {
      LavaMushroomPlatform: None
    }
  ),

  DiveRoom.define(
    locations = {
      "Egg: Moon Cavern - Dive Puzzle": event.Collected(SolvedDivePuzzle)
    },

    region_connections = {
      Main: item.Climb
    }
  )
]