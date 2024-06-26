from typing import override

from ...logic import Entrance, Region, Any
from ...logic import item, tech, carrying
from ...logic.comment import Comment
from ...logic import event
from ...logic import difficulty

class PrismicOutsideDoor(Entrance): pass
class MoonCavernDoor(Entrance): pass
class SunCavernTeleport(Entrance): pass

class Main(Region):
  @override
  @classmethod
  def load(cls):
    from . import MoonCavern

    cls.entrances = [
      MoonCavernDoor.define(MoonCavern.PalaceLobbyDoor)
    ]

    cls.region_connections = {
      Underwater: item.swim,

      Ledges: Any(
        carrying.jester_boots,
        tech.any_super_jump,

        carrying.mr_kerringtons_wings & Any(
          tech.bubble_jump_and_recoil & tech.z_target,
          tech.wing_storage
        ),

        Comment(
          "Hijump double-jump followed by hover",
          tech.ground_tail_jump & item.high_jump & tech.wing_jump
        ),

        item.double_jump & item.wings,

        Comment(
          "Egg iceberg works as a platform",
          event.Collected("Activate Palace Lobby Whirlpool")
        )
      )
    }

class Underwater(Region):
  locations = {
    "Shroom: Palace Lobby - Underwater 1": None,
    "Shroom: Palace Lobby - Underwater 2": None,
    "Shroom: Palace Lobby - Underwater 3": None,
    "Shroom: Palace Lobby - Underwater 4": None,
    "Shroom: Palace Lobby - Underwater 5": None,
    "Shroom: Palace Lobby - Underwater 6": None,

    "Palace Lobby Whirlpool Preston": None,

    "Egg: Palace Lobby - Submerged": None,
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None,

      PrismicEntryPlatform: Any(
        item.sprint,

        item.air_swim,

        carrying.shelnerts_fish | carrying.bubble_conch
      ),

      TopLedge: Any(
        item.air_swim,

        carrying.shelnerts_fish | carrying.bubble_conch
      )
    }

class Ledges(Region):
  locations = {
    "Shroom: Palace Lobby - Ledges 1": None,
    "Shroom: Palace Lobby - Ledges 2": None,
    "Shroom: Palace Lobby - Ledges 3": None,
    "Shroom: Palace Lobby - Ledges 4": None,
    "Shroom: Palace Lobby - Ledges 5": None,
    "Shroom: Palace Lobby - Ledges 6": None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: Any(
        item.wings,
        item.roll & item.air_tail,
        tech.bubble_jump & Any(
          item.high_jump,
          item.sprint,
          item.horn,
          tech.ground_tail_jump,
          tech.air_tail_jump
        )
      ),

      PrismicEntryPlatform: Any(
        event.Collected("Run Palace Lobby Faucet"),

        item.wings & Any(
          item.double_jump,
          item.horn
        ),

        Comment(
          "High + Wing jump from slanted platform to stationary iceberg",
          tech.wing_jump & item.high_jump
        ),

        event.Collected("Activate Palace Lobby Whirlpool") & Any(
          Comment(
            "Precise horn jump from extended ledge onto the tall iceberg. Dive late in the jump arc to gain some extra distance",
            difficulty.hard & item.horn
          ),

          item.air_tail,
          item.ground_tail,

          Comment(
            "Ejection launch from egg iceberg onto tall iceberg as they clip together",
            tech.ejection_launch
          )
        )
      )
    }

class PrismicEntryPlatform(Region):
  @override
  @classmethod
  def load(cls):
    from ..PALACE import PrismicOutside
    from . import SunCavern

    cls.entrances = [
      PrismicOutsideDoor.define(
        default_connection = PrismicOutside.PalaceLobbyDoor
      ),
      SunCavernTeleport.define(
        default_connection = SunCavern.PalaceLobbyTeleport,
        rule = event.Collected("Open Palace Lobby Teleport")
      )
    ]

    cls.region_connections = {
      Ledges: Any(
        event.Collected("Activate Palace Lobby Whirlpool"),
        carrying.mr_kerringtons_wings,

        item.wings,

        tech.bubble_jump & Any(
          item.sprint,
          item.horn,
          tech.ground_tail_jump,
          tech.air_tail_jump
        ),

        Comment(
          "Hijump bubble shot float from the stationary iceberg",
          tech.bubble_jump_and_recoil & item.high_jump
        ),

        item.air_tail & item.roll
      ),

      TopLedge: Any(
        item.horn & item.double_jump,

        carrying.mr_kerringtons_wings & Any(
          tech.wing_storage,
          item.high_jump,
          item.double_jump
        ),

        item.double_jump & item.high_jump & Any(
          tech.ground_tail_jump,

          item.wings
        ),

        tech.bubble_jump_and_recoil & tech.wing_jump & Any(
          tech.ground_tail_jump,

          item.double_jump,
          item.high_jump,
          item.horn,
        )
      )
    }

class TopLedge(Region):
  locations = {
    "Card: Palace Lobby - Top": None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None,
      PrismicEntryPlatform: None,
      Ledges: None
    }
