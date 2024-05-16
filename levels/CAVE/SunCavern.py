from ...logic import templates
from ...logic.whackable import Whackable
from ...logic import Region, Entrance, InternalEvent
from ...logic import All, Any
from ...logic.quantities import HasEggs, HasHearts, HasShrooms
from ...logic.comment import Comment
from ...logic import item, carrying, difficulty, tech, event

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

from . import LostleafLobby
from . import ArmadaLobby
from . import PalaceLobby
from . import GalleryLobby
from ..LAKE import LostleafLake
from . import MoonCavern

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

      "Fed Lostleaf Lake Fella":         HasShrooms("Lake")    & (item.ground_tail | item.air_tail),
      "Fed Airborne Armada Fella":       HasShrooms("Monster") & (item.ground_tail | item.air_tail),
      "Fed Prismic Palace Fella":        HasShrooms("Palace")  & (item.ground_tail | item.air_tail),
      "Fed Gallery of Nightmares Fella": HasShrooms("Gallery") & (item.ground_tail | item.air_tail),
    },

    entrances = [
      LostleafLobbyTeleport.define(
        to = LostleafLobby.SunCavernTeleport,
        rule = event.Collected("Open Lake Lobby Teleport")
      ),

      ArmadaLobbyTeleport.define(
        to = ArmadaLobby.SunCavernTeleport,
        rule = event.Collected("Open Armada Lobby Teleport")
      ),

      PalaceLobbyTeleport.define(
        to = PalaceLobby.SunCavernTeleport,
        rule = event.Collected("Open Palace Lobby Teleport")
      ),

      GalleryLobbyTeleport.define(
        to = GalleryLobby.SunCavernTeleport,
        rule = event.Collected("Open Gallery Lobby Teleport")
      ),
    ],

    region_connections = {
      ArmadaLobbyRoom: Any(
        item.horn,
        item.wings,

        carrying.jester_boots,
        tech.any_super_jump,

        Comment(
          "Well-spaced high jump into the fan",
          item.high_jump & (item.sprint | tech.bubble_jump)
        )
      ),

      HighJumpLedge: Any(
        item.high_jump,
        item.double_jump,

        carrying.jester_boots,
        tech.any_super_jump,

        Comment(
          "Hover-jump into the nearby tutorial stone",
          tech.wing_jump
        ),

        Comment(
          "Build speed and roll into the nearby tutorial stone",
          item.sprint & item.roll
        )
      ),

      VineLedge: Any(
        item.climb,
        tech.any_super_jump,

        Comment(
          "Hover-jump up the sun wall",
          tech.wing_jump
        ),

        Comment(
          "Tail jump double jump from the nearby tutorial stone",
          item.double_jump & Any(
            tech.ground_tail_jump & (item.high_jump | item.wings),
            tech.air_tail_jump & (item.high_jump & item.wings)
          )
        )
      ),

      TailSpinLedge: Any(
        carrying.jester_boots,
        tech.any_super_jump,

        Comment(
          "Roll jump makes the distance",
          item.roll
        ),

        item.high_jump,

        item.bubble,

        item.wings,

        tech.air_tail_jump | tech.ground_tail_jump
      ),

      MightyWallLedge: Any(
        item.climb,
        carrying.jester_boots,
        tech.any_super_jump,

        Comment(
          "Dive-bounce off of shroom",
          item.horn
        ),

        Comment(
          "Jump up a tutorial stone and spire to reach the egg ledge",
          Any(
            item.double_jump & (item.high_jump | item.wings),

            difficulty.intermediate & Any(
              tech.ground_tail_jump,
              tech.air_tail_jump & (item.high_jump | item.double_jump)
            )
          )
        ),
      ),

      WaterfallLedge: Any(
        carrying.jester_boots,
        tech.any_super_jump,

        Comment(
          "Very high jump from one of the nearby gems",
          All (
            difficulty.intermediate,
            tech.ground_tail_jump & item.high_jump & item.double_jump & item.wings
          )
        )
      ),

      DucklingsLedge: Any(
        item.horn,
        item.wings,
        item.double_jump,
        tech.any_super_jump,

        item.roll & (item.sprint | item.air_tail),

        tech.ground_tail_jump,

        Comment(
          "Tail Spin from the right gem to the tiny leaf, then to the big leaf",
          tech.air_tail_jump & Any(
            item.high_jump,
            difficulty.intermediate
          )
        ),
      ),

      DucklingsDoorway: Any(
        tech.any_super_jump,

        Comment(
          "Float to the big leaf from the Sage ramp",
          item.sprint & (tech.wing_jump | tech.bubble_jump)
        ),

        Comment(
          "Jump to the small leaf from the right crystal",
          difficulty.intermediate & tech.air_tail_jump
        ),

        Comment(
          "Speedy launch from the Sage ramp",
          item.sprint & item.roll & item.air_tail
        ),

        Comment(
          "Hover shoot from the Sage ramp",
          tech.wing_jump & tech.bubble_jump_and_recoil
        ),

        Comment(
          "Precise use of bubble float and shoot jumping to land on the leaf from the right gem",
          difficulty.intermediate & tech.bubble_jump
        ),

        tech.momentum_cancel & item.wings,

        Comment(
          "Clever use of wings and riding up the left gem's geometry to jump on a leaf",
          difficulty.intermediate & tech.wing_jump
        )
      ),

      MoonCavernHeartDoorway:
        Comment(
          "Bypass the waterjet",
          item.swim & Any(
            item.horn,
            item.sprint,
            difficulty.intermediate
          )
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
        to = ArmadaLobby.SunCavernDoor
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
        tech.wing_jump,
        item.roll & (item.sprint | item.air_tail)
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
        item.air_tail,
        item.ground_tail,
        carrying.apple,
        carrying.bubble_conch
      ),

      "Egg: Sun Cavern - Mighty Wall": None,

      "Shroom: Sun Cavern - Mighty Wall Egg Ledge 1": None,
      "Shroom: Sun Cavern - Mighty Wall Egg Ledge 2": None,
      "Shroom: Sun Cavern - Mighty Wall Egg Ledge 3": None
    },

    entrances = [
      LostleafLobbyDoor.define(
        to = LostleafLobby.SunCavernDoor,
        rule = event.Collected("Topple Mighty Wall")
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
        to = LostleafLake.DucklingsDoorUpper
      )
    ],

    region_connections = {
      Main: None,

      DucklingsDoorway: Comment(
        "Simply float down",
        tech.bubble_jump | tech.wing_jump
      ),

      MoonCavernHeartDoorway: Comment(
        "Jumping down lets you get past the jets",
        item.swim
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
      DucklingsDoorway: templates.high_jump_obstacle | tech.any_super_jump
    }
  ),

  DucklingsDoorway.define(
    entrances = [
      DucklingsDoorLower.define(
        to = LostleafLake.DucklingsDoorLower
      )
    ],

    region_connections = {
      DucklingsLedge: None
    }
  ),

  MoonCavernHeartDoorway.define(
    entrances = [
      MoonCavernHeartDoor.define(
        to = MoonCavern.SunCavernDoor,
        rule = event.Collected(MoonCavernHeartDoorOpened)
      ),
    ],

    locations = {
      MoonCavernHeartDoorOpened:
        HasHearts(1) & Whackable(ground_tail_works = True, air_tail_works = True)
    },

    region_connections = {
      Main: item.swim,

      DucklingsDoorway:
        Comment(
          "Speedy launch from the waterjet",
          item.swim
        )
    }
  )
]
