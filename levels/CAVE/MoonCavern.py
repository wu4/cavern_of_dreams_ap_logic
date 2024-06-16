from ...logic import Any
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

from . import SunCavern
from . import PalaceLobby
from . import GalleryLobby

regions = [
  Main.define(
    locations = {
      "Card: Moon Cavern - Dive": item.swim & item.horn,

      "Shroom: Moon Cavern - Lava Platforms 1": None,
      "Shroom: Moon Cavern - Lava Platforms 2": None,
      "Shroom: Moon Cavern - Lava Platforms 3": None,
      "Shroom: Moon Cavern - Lava Platforms 4": None,

      "Shroom: Moon Cavern - Potionfall": None,

      SolvedDivePuzzle: item.horn
    },

    entrances = [
      SunCavernDoor.define(
        SunCavern.MoonCavernHeartDoor
      )
    ],

    region_connections = {
      DiveHoles: item.horn,

      DiveRoom: Any(
        item.horn,

        Comment(
          "Vine entrance",
          item.air_tail | carrying.apple | carrying.bubble_conch
        )
      ),

      DivePuzzleLedge: Any(
        tech.any_super_jump,
        carrying.jester_boots,
        carrying.mr_kerringtons_wings,

        item.horn,

        Comment(
          "Extinguish the Keehee and use him as a platform",
          item.bubble
        ),

        item.double_jump & (tech.ground_tail_jump | tech.air_tail_jump),
        item.wings & item.double_jump,

        tech.wing_jump & tech.ground_tail_jump & item.high_jump
      ),

      UpperConnector: Any(
        templates.high_jump_obstacle,
        carrying.mr_kerringtons_wings,

        Comment(
          "Bouncy mushroom + Keehee damage boost",
          tech.damage_boost
        ),

        Comment(
          "Bouncy mushroom + Z-target bubble shooting",
          tech.z_target & tech.bubble_jump
        ),

        Comment(
          "Hover from bouncy shroom",
          item.wings
        )
      ),

      Upper: Any(
        tech.any_super_jump,
        carrying.mr_kerringtons_wings,

        Comment(
          "Hover from bouncy shroom",
          item.wings
        ),

        Comment(
          "Bouncy mushroom + Keehee damage boost while bubble floating",
          tech.damage_boost & tech.bubble_jump
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

      Upper: templates.high_jump_obstacle
    }
  ),

  Upper.define(
    locations = {
      "Egg: Moon Cavern - Keehee Climb": Any(
        tech.any_super_jump,
        carrying.jester_boots,

        item.climb & item.wings & (item.high_jump | item.horn),
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
        PalaceLobby.MoonCavernDoor
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
        tech.any_super_jump,
        templates.high_jump_obstacle,

        carrying.mr_kerringtons_wings,

        tech.bubble_jump_and_recoil & tech.wing_jump,

        Comment(
          "Boost off of the Keehee to the Dive Holes side",
          tech.damage_boost & (difficulty.hard | tech.bubble_jump)
        )
      )
    }
  ),

  NightmareLobbyDoorway.define(
    locations = {
      DousedGalleryLobbyFlame: carrying.medicine | item.bubble
    },

    entrances = [
      GalleryLobbyDoor.define(
        GalleryLobby.MoonCavernDoor,
        Any(
          event.Collected(DousedGalleryLobbyFlame),
          difficulty.hard & tech.damage_boost & tech.momentum_cancel
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
      Main: item.climb
    }
  )
]
