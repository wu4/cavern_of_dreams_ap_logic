from typing import override

from ...logic.objects import Region, Entrance, CarryableLocation
from ...logic.comment import Comment
from ...logic import Any, All
from ...logic import carrying, item, tech, difficulty, event

class SunCavernDoor(Entrance): pass
class EarthDroneCannonShot(Entrance): pass
class EarthDroneCannonShotEarly(Entrance): pass
class SunCavernTeleport(Entrance): pass
class SewerDoor(Entrance): pass

class ArmadaLobbyBoots(CarryableLocation): carryable = "Jester Boots"

class Main(Region):
  locations = {
    "Shroom: Armada Lobby - Cliffside 1": None,
    "Shroom: Armada Lobby - Cliffside 2": None,
    "Shroom: Armada Lobby - Cliffside 3": None,
    "Shroom: Armada Lobby - Cliffside 4": None,
    "Shroom: Armada Lobby - Cliffside 5": None,

    "Card: Armada Lobby - Jester Boots": Any(
      carrying.jester_boots,

      carrying.mr_kerringtons_wings,

      tech.wing_jump & tech.bubble_jump_and_recoil,

      item.double_jump & Any(
        tech.ability_toggle & item.wings,
        item.air_tail & item.roll
      ),

      Comment(
        """
        Precise triple tail-bounce from the walls while z-targeting and
        drifting backwards with bubble float
        """,
        item.air_tail & tech.z_target & tech.bubble_jump & Any(
          difficulty.intermediate & item.double_jump,
          difficulty.hard
        )
      )
    )
  }

  @override
  @classmethod
  def load(cls):
    from . import SunCavern
    from ..MONSTER import EarthDrone

    cls.entrances = [
      SunCavernDoor.define(
        SunCavern.ArmadaLobbyDoor,
        Any(
          tech.roll_disjoint & item.ground_tail,
          carrying.no_jester_boots
        )
      ),
      EarthDroneCannonShotEarly.define(
        EarthDrone.ArmadaLobbyDoor,
        Comment(
          "Early Armada",
          tech.out_of_bounds & carrying.no_jester_boots
        )
      )
    ]

    cls.region_connections = {
      JesterBootsPlatform: Any(
        carrying.jester_boots,
        event.Collected("Raise Armada Lobby Pipes"),
        carrying.mr_kerringtons_wings,
        item.wings,
        item.double_jump,
        tech.ground_tail_jump,
        tech.air_tail_jump & (difficulty.intermediate | item.high_jump),
        item.air_tail & item.roll,
        item.sprint & item.horn,
        Comment(
          "Ejection launch from cannon wheel",
          tech.ejection_launch & item.roll
        )
      ),

      CannonLip: Any(
        tech.any_super_jump,

        All(
          event.Collected("Activate Armada Lobby Red Pipe Updraft"),
          event.Collected("Raise Armada Lobby Pipes"),
          item.wings
        ),

        item.double_jump & Any(
          Comment(
            "Fly up to the tree trunk in the back",
            tech.wing_jump & carrying.mr_kerringtons_wings,
          ),

          item.horn,
          item.high_jump,
          item.wings,
          tech.ground_tail_jump,
          tech.air_tail_jump & difficulty.intermediate,
        )
      ),

      FlagPlatform: Any(
        carrying.jester_boots,
        carrying.mr_kerringtons_wings,
        Comment(
          "Wing Storage from slope on entry pipe",
          tech.wing_jump & tech.wing_storage,
        ),

        item.double_jump,
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump & (item.high_jump | item.wings | tech.bubble_jump),

        Comment(
          "Wings + Bubble shoot onto and from the entrance pipe",
          tech.wing_jump & tech.bubble_jump_and_recoil
        )
      )
    }

class JesterBootsPlatform(Region):
  locations = {
    ArmadaLobbyBoots: Any(
      item.ground_tail,
      item.air_tail,
      carrying.apple | carrying.bubble_conch,
      # The wall allows destroying it with the horn, but it's impossible
      # to actually do it
      # item.horn
    )
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: Any(
        tech.any_super_jump,
        carrying.jester_boots,
        carrying.mr_kerringtons_wings,
        item.wings,
        Comment(
          "Leap from the red pipe to the right wheel",
          event.Collected("Raise Armada Lobby Pipes"),
        ),

        item.high_jump,
        item.air_tail,
        tech.ground_tail_jump,
        item.horn,
        item.sprint,
        tech.bubble_jump,
        item.double_jump
      )
    }

class CannonLip(Region):
  @override
  @classmethod
  def load(cls):
    from . import SunCavern
    from ..MONSTER import EarthDrone

    cls.entrances = [
      SunCavernTeleport.define(
        default_connection = SunCavern.ArmadaLobbyTeleport,
        rule = event.Collected("Open Armada Lobby Teleport"),
      ),
      EarthDroneCannonShot.define(
        default_connection = EarthDrone.ArmadaLobbyDoor,
        rule = carrying.no_jester_boots
      )
    ]

    cls.region_connections = {
      Main: None,

      EggPlatform: Any(
        carrying.jester_boots,
        tech.any_super_jump,

        Comment(
          """
          Hover jump towards the pipe, enable double-jump, then jump onto the
          pipe. Perform the same trick from the pipe to the ledge
          """,
          tech.wing_jump & (carrying.mr_kerringtons_wings | tech.ability_toggle) & item.double_jump
        ),

        Comment(
          """
          Double jump and hover-shoot to the pipe, then do the same to the
          platform
          """,
          tech.wing_jump & tech.bubble_jump_and_recoil & item.double_jump
        ),

        Comment(
          """
          Speedy roll launch to the pipe and double jump, then do the same to
          the platform
          """,
          item.air_tail & item.roll & item.double_jump
        )
      )
    }

class FlagPlatform(Region):
  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None,
      SewerConnector: item.swim
    }

class SewerConnector(Region):
  @override
  @classmethod
  def load(cls):
    from . import Sewer

    cls.entrances = [
      SewerDoor.define(
        default_connection = Sewer.ArmadaLobbyDoor
      )
    ]

    cls.region_connections = {
      FlagPlatform: item.swim
    }

class EggPlatform(Region):
  locations = {
    "Egg: Armada Lobby - Cannon": None,
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      CannonLip: None
    }
