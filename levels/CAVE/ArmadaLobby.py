from ...logic.objects import Region, Entrance, JesterBoots
from ...logic.comment import Comment
from ...logic import Any, All
from ...logic import carrying, item, tech, difficulty, event, whackable

class Main(Region): pass
class JesterBootsPlatform(Region): pass
class CannonLip(Region): pass
class FlagPlatform(Region): pass
class SewerConnector(Region): pass
class EggPlatform(Region): pass

class SunCavernDoor(Entrance): pass
class EarthDroneCannonShot(Entrance): pass
class EarthDroneCannonShotEarly(Entrance): pass
class SunCavernTeleport(Entrance): pass
class SewerDoor(Entrance): pass

class ArmadaLobbyBoots(JesterBoots): pass

from . import SunCavern as _SunCavern
from . import Sewer as _Sewer
from ..MONSTER import EarthDrone as _EarthDrone

regions = [
  Main.define(
    locations = {
      "Shroom: Armada Lobby - Cliffside 1": None,
      "Shroom: Armada Lobby - Cliffside 2": None,
      "Shroom: Armada Lobby - Cliffside 3": None,
      "Shroom: Armada Lobby - Cliffside 4": None,
      "Shroom: Armada Lobby - Cliffside 5": None,

      "Card: Armada Lobby - Jester Boots": Any(
        carrying.JesterBoots,
        tech.HoverShoot,
        item.DoubleJump & Any(
          tech.AbilityToggle & item.Wings,
          item.AirTail & item.Roll
        ),
        Comment(
          """
          Precise triple tail-bounce from the walls while z-targeting and
          drifting backwards with bubble float
          """,
          item.AirTail & tech.ZTarget & tech.BubbleJump & Any(
            difficulty.Intermediate & item.DoubleJump,
            difficulty.Hard
          )
        )
      )
    },

    entrances = [
      SunCavernDoor.define(
        _SunCavern.ArmadaLobbyDoor,
        tech.RollDisjoint(requires_tail = True) | carrying.NoJesterBoots
      ),
      EarthDroneCannonShotEarly.define(
        _EarthDrone.ArmadaLobbyDoor,
        Comment(
          "Early Armada",
          tech.OutOfBounds
        )
      )
    ],

    region_connections = {
      JesterBootsPlatform: Any(
        carrying.JesterBoots,
        event.Collected("Raise Armada Lobby Pipes"),
        item.Wings,
        item.DoubleJump,
        tech.GroundTailJump,
        tech.AirTailJump & (difficulty.Intermediate | item.HighJump),
        item.AirTail & item.Roll,
        item.Sprint & item.Horn,
        Comment(
          "Ejection launch from cannon wheel",
          tech.EjectionLaunch & item.Roll
        )
      ),

      CannonLip: Any(
        tech.AnySuperJump,

        All(
          event.Collected("Activate Armada Lobby Red Pipe Updraft"),
          event.Collected("Raise Armada Lobby Pipes"),
          item.Wings
        ),

        item.DoubleJump & Any(
          item.Horn,
          item.HighJump,
          item.Wings,
          tech.GroundTailJump,
          tech.AirTailJump & difficulty.Intermediate,
        )
      ),

      FlagPlatform: Any(
        carrying.JesterBoots,
        tech.AnySuperJump,

        item.DoubleJump,
        item.Horn,
        tech.GroundTailJump,
        tech.AirTailJump & item.HighJump,

        Comment(
          "Hover shoot onto and from the entrance pipe",
          tech.HoverShoot
        )
      )
    },
  ),

  FlagPlatform.define(
    region_connections = {
      Main: None,
      SewerConnector: item.Swim
    }
  ),

  SewerConnector.define(
    entrances = [
      SewerDoor.define(_Sewer.ArmadaLobbyDoor)
    ],

    region_connections = {
      FlagPlatform: item.Swim
    }
  ),

  JesterBootsPlatform.define(
    locations = {
      ArmadaLobbyBoots: whackable.Whackable(
        ground_tail_works = True,
        air_tail_works = True,
        roll_works = True,
        throwable_works = True,
        # horn_works = True
      )
    },

    region_connections = {
      # death warp
      Main: None
    }
  ),

  CannonLip.define(
    entrances = [
      SunCavernTeleport.define(
        to = _SunCavern.ArmadaLobbyTeleport,
        rule = event.Collected("Open Armada Lobby Teleport"),
      ),
      EarthDroneCannonShot.define(
        to = _EarthDrone.ArmadaLobbyDoor,
        rule = None
      )
    ],

    region_connections = {
      Main: None,
      EggPlatform: Any(
        carrying.JesterBoots,
        tech.AnySuperJump,

        Comment(
          """
          Hover jump towards the pipe, enable double-jump, then jump onto the
          pipe. Perform the same trick from the pipe to the ledge
          """,
          tech.HoverJump & tech.AbilityToggle & item.DoubleJump
        ),

        Comment(
          """
          Double jump and hover-shoot to the pipe, then do the same to the
          platform
          """,
          tech.HoverShoot & item.DoubleJump
        ),

        Comment(
          """
          Speedy roll launch to the pipe and double jump, then do the same to
          the platform
          """,
          item.AirTail & item.Roll & item.DoubleJump
        )
      )
    }
  ),

  EggPlatform.define(
    locations = {
      "Egg: Armada Lobby - Cannon": None,
    },

    region_connections = {
      CannonLip: None
    }
  )
]
