from ...logic import Entrance, Region, Any
from ...logic import item, tech, carrying
from ...logic.comment import Comment
from ...logic.event import Collected as EventCollected

class PrismicOutsideDoor(Entrance): pass
class MoonCavernDoor(Entrance): pass
class SunCavernTeleport(Entrance): pass

from . import SunCavern
from . import MoonCavern
from ..PALACE import PrismicOutside

class Main(Region): pass
class Underwater(Region): pass
class Ledges(Region): pass
class PrismicEntryPlatform(Region): pass

regions = [
  Main.define(
    entrances = [
      MoonCavernDoor.define(MoonCavern.PalaceLobbyDoor)
    ],

    region_connections = {
      Underwater: item.swim,

      Ledges: Any(
        carrying.jester_boots,
        tech.any_super_jump,
        Comment(
          "Hijump double-jump followed by hover",
          tech.ground_tail_jump & item.high_jump & tech.wing_jump
        ),

        item.double_jump & item.wings,

        Comment(
          "Egg iceberg works as a platform",
          EventCollected("Activate Palace Lobby Whirlpool")
        )
      )
    }
  ),

  PrismicEntryPlatform.define(
    entrances = [
      PrismicOutsideDoor.define(PrismicOutside.PalaceLobbyDoor)
    ],

    region_connections = {
      Ledges: Any(
        EventCollected("Activate Palace Lobby Whirlpool"),
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
      )
    }
  ),

  Ledges.define(
    locations = {
      "Shroom: Palace Lobby - Ledges 1": None,
      "Shroom: Palace Lobby - Ledges 2": None,
      "Shroom: Palace Lobby - Ledges 3": None,
      "Shroom: Palace Lobby - Ledges 4": None,
      "Shroom: Palace Lobby - Ledges 5": None,
      "Shroom: Palace Lobby - Ledges 6": None
    },

    region_connections = {
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
      )
    }
  )
]
