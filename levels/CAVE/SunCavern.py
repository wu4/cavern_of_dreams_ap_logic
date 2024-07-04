from ...logic.quantities import HasEggs, HasGratitude, HasShrooms
from ...logic.comment import Comment
from ...logic.objects import EntranceType
from ...logic import lazy_region, Region, Entrance, InternalEvent, All, Any
from ...logic import item, carrying, difficulty, tech, event, templates

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

@lazy_region
def Main(r: Region):
  r.locations = {
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

    "Fed Lostleaf Lake Fella":         HasShrooms("Lake")    & (item.ground_tail | item.air_tail | item.horn),
    "Fed Airborne Armada Fella":       HasShrooms("Monster") & (item.ground_tail | item.air_tail | item.horn),
    "Fed Prismic Palace Fella":        HasShrooms("Palace")  & (item.ground_tail | item.air_tail | item.horn),
    "Fed Gallery of Nightmares Fella": HasShrooms("Gallery") & (item.ground_tail | item.air_tail | item.horn),
  }

  from . import LostleafLobby, ArmadaLobby, PalaceLobby, GalleryLobby

  r.entrances = [
    LostleafLobbyTeleport.define(
      default_connection = LostleafLobby.SunCavernTeleport,
      rule = event.Collected("Open Lake Lobby Teleport") & carrying.no_jester_boots
    ),

    ArmadaLobbyTeleport.define(
      default_connection = ArmadaLobby.SunCavernTeleport,
      rule = event.Collected("Open Armada Lobby Teleport") & carrying.no_jester_boots
    ),

    PalaceLobbyTeleport.define(
      default_connection = PalaceLobby.SunCavernTeleport,
      rule = event.Collected("Open Palace Lobby Teleport") & carrying.no_jester_boots
    ),

    GalleryLobbyTeleport.define(
      default_connection = GalleryLobby.SunCavernTeleport,
      rule = event.Collected("Open Gallery Lobby Teleport") & carrying.no_jester_boots
    ),
  ]

  r.region_connections = {
    ArmadaLobbyRoom: Any(
      item.horn,
      item.wings,
      carrying.mr_kerringtons_wings,

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
      ),

      Comment(
        "Wing storage + double jump from the nearby tutorial stone",
        tech.wing_storage & item.double_jump
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
        """
        Hover-jump up the sun wall to the red eyes, then float from the
        crystal
        """,
        tech.wing_jump & carrying.mr_kerringtons_wings
      ),

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
      carrying.mr_kerringtons_wings,
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
      carrying.mr_kerringtons_wings,

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
          carrying.bubble_conch,
          carrying.shelnerts_fish,
          difficulty.intermediate
        )
      )
  }

@lazy_region
def ArmadaLobbyRoom(r: Region):
  r.locations = {
    "Shroom: Sun Cavern - Armada Entrance 1" : None,
    "Shroom: Sun Cavern - Armada Entrance 2" : None,
    "Shroom: Sun Cavern - Armada Entrance 3" : None,
  }

  from . import ArmadaLobby

  r.entrances = [
    ArmadaLobbyDoor.define(
      default_connection = ArmadaLobby.SunCavernDoor
    )
  ]

  r.region_connections = {
    Main: None
  }

@lazy_region
def HighJumpLedge(r: Region):
  r.locations = {
    "Shroom: Sun Cavern - High Jump Ledge 1": None,
    "Shroom: Sun Cavern - High Jump Ledge 2": None
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def VineLedge(r: Region):
  r.locations = {
    "Shroom: Sun Cavern - Vine Ledge 1": None,
    "Shroom: Sun Cavern - Vine Ledge 2": None
  }

  r.region_connections = {
    Main: None,
    HighJumpLedge: Any(
      tech.wing_jump,
      item.roll & (item.sprint | item.air_tail)
    )
  }

@lazy_region
def TailSpinLedge(r: Region):
  r.locations = {
    "Shroom: Sun Cavern - Tail Spin Ledge 1": None,
    "Shroom: Sun Cavern - Tail Spin Ledge 2": None
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def MightyWallLedge(r: Region):
  r.locations = {
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
  }

  from . import LostleafLobby

  r.entrances = [
    LostleafLobbyDoor.define(
      default_connection = LostleafLobby.SunCavernDoor,
      rule = event.Collected("Topple Mighty Wall")
    )
  ]

  r.region_connections = {
    Main: None
  }

@lazy_region
def WaterfallLedge(r: Region):
  r.locations = {
    "Egg: Sun Cavern - Waterfall": None
  }

  from ..LAKE import LostleafLake

  r.entrances = [
    DucklingsDoorUpper.define(
      default_connection = LostleafLake.DucklingsDoorUpper
    )
  ]

  r.region_connections = {
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

@lazy_region
def DucklingsLedge(r: Region):
  r.locations = {
    "Shroom: Sun Cavern - Ducklings Ledge 1": None,
    "Shroom: Sun Cavern - Ducklings Ledge 2": None
  }

  r.region_connections = {
    Main: None,
    DucklingsDoorway: templates.high_jump_obstacle | tech.any_super_jump
  }

@lazy_region
def DucklingsDoorway(r: Region):
  from ..LAKE import LostleafLake

  r.entrances = [
    DucklingsDoorLower.define(
      default_connection = LostleafLake.DucklingsDoorLower
    )
  ]

  r.region_connections = {
    DucklingsLedge: None
  }

@lazy_region
def MoonCavernHeartDoorway(r: Region):
  r.locations = {
    MoonCavernHeartDoorOpened:
      HasGratitude(1) & (item.ground_tail | item.air_tail)
  }

  from . import MoonCavern

  r.entrances = [
    MoonCavernHeartDoor.define(
      default_connection = MoonCavern.SunCavernDoor,
      rule = event.Collected(MoonCavernHeartDoorOpened),
      type = EntranceType.BILINEAR | EntranceType.UNDERWATER
    ),
  ]

  r.region_connections = {
    Main: item.swim,

    DucklingsDoorway:
      Comment(
        "Speedy launch from the waterjet",
        item.swim
      )
  }
