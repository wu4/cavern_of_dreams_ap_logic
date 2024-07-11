from ...logic.objects import lazy_region, Region, Entrance, CarryableLocation
from ...logic.comment import Comment
from ...logic import Any, All
from ...logic import carrying, item, tech, difficulty, event

area_path = "CAVE/Monster Lobby"

class SunCavernDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromMonsterLobbyToCave"
  dest_path = f"{area_path}/Warps/DestFromCaveToMonsterLobby"
class EarthDroneCannonShot(Entrance):
  warp_path = f"{area_path}/Cutscenes/CannonShot/WarpEvent"
  dest_path = f"{area_path}/Warps/DestFromDroneEarthToMonsterLobby"
class SewerDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromMonsterLobbyToCave"
  dest_path = f"{area_path}/Warps/DestFromCaveToMonsterLobby"
class SunCavernTeleport(Entrance):
  warp_path = f"{area_path}/Warps/Portal"
  dest_path = f"{warp_path}/DestFromPortal???"

class ArmadaLobbyBoots(CarryableLocation): carryable = "Jester Boots"

@lazy_region
def Main(r: Region):
  r.locations = {
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

  from . import SunCavern

  r.entrances = [
    SunCavernDoor.define(
      SunCavern.ArmadaLobbyDoor,
      Any(
        tech.roll_disjoint & item.ground_tail,
        carrying.no_jester_boots
      )
    )
  ]

  r.region_connections = {
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

    EnterCannon: Comment(
      "Early Armada",
      tech.out_of_bounds & carrying.no_jester_boots
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

@lazy_region
def JesterBootsPlatform(r: Region):
  r.locations = {
    ArmadaLobbyBoots: Any(
      item.ground_tail,
      item.air_tail,
      carrying.apple | carrying.bubble_conch,
      # The wall allows destroying it with the horn, but it's impossible
      # to actually do it
      # item.horn
    )
  }

  r.region_connections = {
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

@lazy_region
def EnterCannon(r: Region):
  from ..MONSTER import EarthDrone

  r.entrances = [
    EarthDroneCannonShot.define(
      default_connection = EarthDrone.ArmadaLobbyDoor,
      rule = carrying.no_jester_boots
    )
  ]

  r.region_connections = {
    CannonLip: None
  }

@lazy_region
def CannonLip(r: Region):
  from . import SunCavern

  r.entrances = [
    SunCavernTeleport.define(
      default_connection = SunCavern.ArmadaLobbyTeleport,
      rule = event.Collected("Open Armada Lobby Teleport"),
    ),
  ]

  r.region_connections = {
    Main: None,
    EnterCannon: None,

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

@lazy_region
def FlagPlatform(r: Region):
  r.region_connections = {
    Main: None,
    SewerConnector: item.swim
  }

@lazy_region
def SewerConnector(r: Region):
  from . import Sewer

  r.entrances = [
    SewerDoor.define(
      default_connection = Sewer.ArmadaLobbyDoor
    )
  ]

  r.region_connections = {
    FlagPlatform: item.swim
  }

@lazy_region
def EggPlatform(r: Region):
  r.locations = {
    "Egg: Armada Lobby - Cannon": None,
  }

  r.region_connections = {
    CannonLip: None
  }
