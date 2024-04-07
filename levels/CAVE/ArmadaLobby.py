from ...logic import *

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
        Carrying("Jester Boots"),
        CanHoverShoot,
        HasDoubleJump & Any(
          Tech("ability_toggle") & HasWings,
          HasAirTail & HasRoll
        ),
        Comment("""
          Precise triple tail-bounce from the walls while z-targeting and
          drifting backwards with bubble float
          """,
          HasAirTail & Tech("z_target") & CanBubbleJump & Any(
            Difficulty("Hard"),
            Difficulty("Intermediate") & HasDoubleJump
          )
        )
      )
    },

    entrances = [
      SunCavernDoor.define(
        _SunCavern.ArmadaLobbyDoor,
        CanRollDisjoint(requires_tail = True) | NoJesterBoots
      ),
      EarthDroneCannonShotEarly.define(
        _EarthDrone.ArmadaLobbyDoor,
        Comment(
          "Early Armada",
          Tech("out_of_bounds")
        )
      )
    ],

    region_connections = {
      JesterBootsPlatform: Any(
        Carrying("Jester Boots"),
        Has("Raise Armada Lobby Pipes"),
        HasWings,
        HasDoubleJump,
        CanTailJump(
          aerialExtraLogic = Difficulty("Intermediate") | HasHighJump
        ),
        HasAirTail & HasRoll,
        HasSprint & HasHorn,
        Comment(
          "Ejection launch from cannon wheel",
          Tech("ejection_launch") & HasRoll
        )
      ),

      CannonLip: Any(
        CanSuperJump,

        All(
          Has("Activate Armada Lobby Red Pipe Updraft"),
          Has("Raise Armada Lobby Pipes"),
          HasWings
        ),

        HasDoubleJump & Any(
          HasHorn,
          HasHighJump,
          HasWings,
          CanTailJump(
            aerialExtraLogic = Difficulty("Intermediate")
          )
        )
      ),

      FlagPlatform: Any(
        Carrying("Jester Boots"),
        CanSuperJump,

        HasDoubleJump,
        HasHorn,
        CanTailJump(
          aerialExtraLogic = HasHighJump
        ),

        Comment(
          "Hover shoot onto and from the entrance pipe",
          CanHoverShoot
        )
      )
    },
  ),

  FlagPlatform.define(
    region_connections = {
      Main: None,
      SewerConnector: HasSwim
    }
  ),

  SewerConnector.define(
    entrances = [
      SewerDoor.define(_Sewer.ArmadaLobbyDoor)
    ],

    region_connections = {
      FlagPlatform: HasSwim
    }
  ),

  JesterBootsPlatform.define(
    locations = {
      ArmadaLobbyBoots: Whackable(
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
        rule = Has("Open Armada Lobby Teleport")
      ),
      EarthDroneCannonShot.define(
        to = _EarthDrone.ArmadaLobbyDoor,
        rule = None
      )
    ],

    region_connections = {
      Main: None,
      EggPlatform: Any(
        Carrying("Jester Boots"),
        CanSuperJump,
        
        Comment(
          """
          Hover jump towards the pipe, enable double-jump, then jump onto the
          pipe. Perform the same trick from the pipe to the ledge
          """,
          CanHoverJump & Tech("ability_toggle") & HasDoubleJump
        ),
    
        Comment(
          """
          Double jump and hover-shoot to the pipe, then do the same to the
          platform
          """,
          CanHoverShoot & HasDoubleJump
        ),

        Comment(
          """
          Speedy roll launch to the pipe and double jump, then do the same to
          the platform
          """,
          HasAirTail & HasRoll & HasDoubleJump
        )
      )
    }
  ),
  
  EggPlatform.define(
    locations = {
      "Egg: Armada Lobby - Cannon": None
    },

    region_connections = {
      CannonLip: None
    }
  )
]