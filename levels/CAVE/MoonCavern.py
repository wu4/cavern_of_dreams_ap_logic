from typing import override

from ...logic.objects import Region, Entrance, InternalEvent
from ...logic import Any
from ...logic import item, event, difficulty, carrying, tech, templates
from ...logic.comment import Comment

class SunCavernDoor(Entrance): pass
class PalaceLobbyDoor(Entrance): pass
class GalleryLobbyDoor(Entrance): pass

class DousedGalleryLobbyFlame(InternalEvent): pass
class SolvedDivePuzzle(InternalEvent): pass

class Main(Region):
  locations = {
    "Card: Moon Cavern - Dive": item.swim & item.horn,

    "Shroom: Moon Cavern - Lava Platforms 1": None,
    "Shroom: Moon Cavern - Lava Platforms 2": None,
    "Shroom: Moon Cavern - Lava Platforms 3": None,
    "Shroom: Moon Cavern - Lava Platforms 4": None,

    "Shroom: Moon Cavern - Potionfall": None,

    SolvedDivePuzzle: item.horn
  }

  @override
  @classmethod
  def load(cls):
    from . import SunCavern

    cls.entrances = [
      SunCavernDoor.define(
        SunCavern.MoonCavernHeartDoor
      )
    ]

    cls.region_connections = {
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

class DiveRoom(Region):
  locations = {
    "Egg: Moon Cavern - Dive Puzzle": event.Collected(SolvedDivePuzzle)
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: item.climb
    }

class DivePuzzleLedge(Region):
  locations = {
    "Shroom: Moon Cavern - Dive Puzzle 1": None,
    "Shroom: Moon Cavern - Dive Puzzle 2": None,
    "Shroom: Moon Cavern - Dive Puzzle 3": None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None
    }

class UpperConnector(Region):
  locations = {
    "Shroom: Moon Cavern - Lonely Shroom": None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None,

      Upper: templates.high_jump_obstacle
    }

class Upper(Region):
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
  }

  @override
  @classmethod
  def load(cls):
    from . import PalaceLobby

    cls.entrances = [
      PalaceLobbyDoor.define(
        PalaceLobby.MoonCavernDoor
      )
    ]

    cls.region_connections = {
      UpperConnector: None
    }

class LavaMushroomPlatform(Region):
  locations = {
    "Shroom: Moon Cavern - Lava Mushroom Platform 1": None,
    "Shroom: Moon Cavern - Lava Mushroom Platform 2": None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
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

class DiveHoles(Region):
  locations = {
    "Shroom: Moon Cavern - Dive Holes 1": None,
    "Shroom: Moon Cavern - Dive Holes 2": None,
    "Shroom: Moon Cavern - Dive Holes 3": None,
    "Shroom: Moon Cavern - Dive Holes 4": None,
    "Shroom: Moon Cavern - Dive Holes 5": None,
    "Shroom: Moon Cavern - Dive Holes 6": None,
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None
    }

class NightmareLobbyDoorway(Region):
  locations = {
    DousedGalleryLobbyFlame: carrying.medicine | item.bubble
  }

  @override
  @classmethod
  def load(cls):
    from . import GalleryLobby

    cls.entrances = [
      GalleryLobbyDoor.define(
        GalleryLobby.MoonCavernDoor,
        Any(
          event.Collected(DousedGalleryLobbyFlame),
          difficulty.hard & tech.damage_boost & tech.momentum_cancel
        )
      )
    ]

    cls.region_connections = {
      LavaMushroomPlatform: None
    }
