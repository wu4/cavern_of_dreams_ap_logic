from ...logic.objects import Region, Entrance, JesterBootsLocation
from ...logic.comment import Comment
from ...logic import Any, All
from ...logic import carrying, item, tech, difficulty, event, whackable

sun_cavern_door = Entrance("Sun Cavern Door")
earth_drone_cannon_shot = Entrance("Earth Drone Cannon Shot")
earth_drone_cannon_shot_clip = Entrance("Earth Drone Cannon Shot (Clip)")
sun_cavern_teleport = Entrance("Sun Cavern Teleport")
sewer_door = Entrance("Sewer Door")

boots_location = JesterBootsLocation("Armada Lobby Boots")

from . import SunCavern
from . import Sewer
from ..MONSTER import EarthDrone

main = Region("Main")
jester_boots_platform = Region("Jester Boots Platform")
cannon_lip = Region("Cannon Lip")
flag_platform = Region("Flag Platform")
sewer_connector = Region("Sewer Connector")
egg_platform = Region("Egg Platform")

regions = [
  main.define(
    locations = {
      "Shroom: Armada Lobby - Cliffside 1": None,
      "Shroom: Armada Lobby - Cliffside 2": None,
      "Shroom: Armada Lobby - Cliffside 3": None,
      "Shroom: Armada Lobby - Cliffside 4": None,
      "Shroom: Armada Lobby - Cliffside 5": None,

      "Card: Armada Lobby - Jester Boots": Any(
        carrying.jester_boots,
        tech.hover_shoot,
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
    },

    entrances = [
      sun_cavern_door.define(
        SunCavern.ArmadaLobbyDoor,
        tech.roll_disjoint(requires_tail = True) | carrying.no_jester_boots
      ),
      earth_drone_cannon_shot_clip.define(
        EarthDrone.ArmadaLobbyDoor,
        Comment(
          "Early Armada",
          tech.out_of_bounds
        )
      )
    ],

    region_connections = {
      jester_boots_platform: Any(
        carrying.jester_boots,
        event.Collected("Raise Armada Lobby Pipes"),
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

      cannon_lip: Any(
        tech.any_super_jump,

        All(
          event.Collected("Activate Armada Lobby Red Pipe Updraft"),
          event.Collected("Raise Armada Lobby Pipes"),
          item.wings
        ),

        item.double_jump & Any(
          item.horn,
          item.high_jump,
          item.wings,
          tech.ground_tail_jump,
          tech.air_tail_jump & difficulty.intermediate,
        )
      ),

      flag_platform: Any(
        carrying.jester_boots,
        tech.any_super_jump,

        item.double_jump,
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump & item.high_jump,

        Comment(
          "Hover shoot onto and from the entrance pipe",
          tech.hover_shoot
        )
      )
    },
  ),

  flag_platform.define(
    region_connections = {
      main: None,
      sewer_connector: item.swim
    }
  ),

  sewer_connector.define(
    entrances = [
      sewer_door.define(Sewer.armada_lobby_door)
    ],

    region_connections = {
      flag_platform: item.swim
    }
  ),

  jester_boots_platform.define(
    locations = {
      boots_location: whackable.Whackable(
        ground_tail_works = True,
        air_tail_works = True,
        roll_works = True,
        throwable_works = True,
        # horn_works = True
      )
    },

    region_connections = {
      # death warp
      main: None
    }
  ),

  cannon_lip.define(
    entrances = [
      sun_cavern_teleport.define(
        to = SunCavern.ArmadaLobbyTeleport,
        rule = event.Collected("Open Armada Lobby Teleport"),
      ),
      earth_drone_cannon_shot.define(
        to = EarthDrone.ArmadaLobbyDoor,
        rule = None
      )
    ],

    region_connections = {
      main: None,
      egg_platform: Any(
        carrying.jester_boots,
        tech.any_super_jump,

        Comment(
          """
          Hover jump towards the pipe, enable double-jump, then jump onto the
          pipe. Perform the same trick from the pipe to the ledge
          """,
          tech.hover_jump & tech.ability_toggle & item.double_jump
        ),

        Comment(
          """
          Double jump and hover-shoot to the pipe, then do the same to the
          platform
          """,
          tech.hover_shoot & item.double_jump
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
  ),

  egg_platform.define(
    locations = {
      "Egg: Armada Lobby - Cannon": None,
    },

    region_connections = {
      cannon_lip: None
    }
  )
]
