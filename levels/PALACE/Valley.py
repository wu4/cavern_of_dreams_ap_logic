from ...logic.comment import Comment
from ...logic import lazy_region, Region, Entrance, InternalEvent, Any, CarryableLocation
from ...logic.logic import Not
from ...logic import item, carrying, difficulty, tech, event, templates

area_path = "PALACE/Valley (Main)"

class LostleafDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromValleyToLake"
  dest_path = f"{area_path}/Warps/DestFromLakeToValley"
class PalaceLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromValleyToPalaceLobby"
  dest_path = f"{area_path}/Warps/DestFromPalaceLobbyToValley"
class SanctumDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromValleyTopToSanctum"
  dest_path = f"{area_path}/Warps/DestFromSanctumToValleyTop"
class DiningRoomDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromValleyToDiningRoom"
  dest_path = f"{area_path}/Warps/DestFromDiningRoomToValley"
class ObservatoryShortcutDoorBottom(Entrance):
  warp_path = f"{area_path}/Warps/WarpObservatoryBottomToTop"
  dest_path = f"{area_path}/Warps/DestObservatoryBottomToTop"
class ObservatoryShortcutDoorTop(Entrance):
  warp_path = f"{area_path}/Warps/WarpObservatoryTopToBottom"
  dest_path = f"{area_path}/Warps/DestObservatoryTopToBottom"
class ObservatoryDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromValleyToObservatory"
  dest_path = f"{area_path}/Warps/DestFromObservatoryToValley"
class PalaceFrontDoor(Entrance):
  is_dest_underwater = True
  warp_path = f"{area_path}/Warps/WarpFromValleyToPalace"
  dest_path = f"{area_path}/Warps/DestFromPalaceToValley"
class PalaceBasementDoor(Entrance):
  is_dest_underwater = True
  warp_path = f"{area_path}/Warps/WarpFromAbyssToPalace"
  dest_path = f"{area_path}/Warps/DestFromPalaceToAbyss"

class ValleyJesterBoots(CarryableLocation): carryable = "Jester Boots"
class AirSwimFromLostleafEntryway(InternalEvent): pass
class UnstuckBigstar(InternalEvent): pass
class BrokeLowerWaterWall(InternalEvent): pass

CanAirSwim = Any(
    event.Collected(AirSwimFromLostleafEntryway),
    event.Collected("Unfreeze Prismic Palace") & item.swim & item.air_swim & tech.momentum_cancel
)

@lazy_region
def Main(r: Region):
  r.locations = {
    "Shroom: Prismic Palace - Entry 1": None,
    "Shroom: Prismic Palace - Entry 2": None,
    "Shroom: Prismic Palace - Entry 3": None,

    "Shroom: Prismic Palace - Pool Bridges 1": None,
    "Shroom: Prismic Palace - Pool Bridges 2": None,
    "Shroom: Prismic Palace - Pool Bridges 3": None,
    "Shroom: Prismic Palace - Pool Bridges 4": None,
    "Shroom: Prismic Palace - Pool Bridges 5": None,
    "Shroom: Prismic Palace - Pool Bridges 6": None,

    "Shroom: Prismic Palace - Poki-Poki Cave 1": None,
    "Shroom: Prismic Palace - Poki-Poki Cave 2": None,
    "Shroom: Prismic Palace - Poki-Poki Cave 3": None,
    "Shroom: Prismic Palace - Poki-Poki Cave 4": None,
    "Shroom: Prismic Palace - Poki-Poki Cave 5": None,

    "Prismic Palace - Help Lady Opal":
      item.lady_opal_egg_1 & item.lady_opal_egg_2 & item.lady_opal_egg_3,
  }

  from ..CAVE import PalaceLobby

  r.entrances = [
    PalaceLobbyDoor.define(PalaceLobby.ValleyDoor),
    ObservatoryShortcutDoorBottom.define(
      default_connection = ObservatoryShortcutDoorTop,
      rule = event.Collected("Open Observatory Shortcut")
    )
  ]

  r.region_connections = {
    OuterRim: CanAirSwim,

    UpperWater: event.Collected("Unfreeze Prismic Palace") & item.swim,

    ClipIntoIce: tech.out_of_bounds & item.swim,

    Spires: Any(
      CanAirSwim,
      tech.any_super_jump,
      item.climb
    ),

    PoolCardLedge: Any(
      CanAirSwim,
      tech.any_super_jump
    ),

    JesterBootsCoveDryJBRemovalField: Any(
      carrying.jester_boots,
      item.climb,
      tech.wing_storage,
      templates.high_jump_obstacle,
      tech.wing_jump & tech.bubble_jump_and_recoil
    ),

    Pool: item.swim & Any(
      item.horn,
      event.Collected("Unfreeze Prismic Palace")
    ),

    EntrancePomLedge: Any(
      carrying.jester_boots,
      tech.super_bubble_jump,

      item.climb,
      item.double_jump,
      tech.ground_tail_jump,
      tech.air_tail_jump & (item.high_jump | tech.bubble_jump),
      item.horn
    ),

    PokiPokiCave: Any(
      difficulty.intermediate,
      item.climb,
      tech.air_tail_jump,
      tech.ground_tail_jump,
      item.double_jump,
      item.high_jump & Any(
        tech.wing_jump,
      )
    )
  }

@lazy_region
def JesterBootsCoveDryJBRemovalField(r: Region):
  r.region_connections = {
    Main: carrying.no_jester_boots,
    JesterBootsCoveLowerPlatforms: carrying.no_jester_boots
  }

@lazy_region
def Pool(r: Region):
  r.locations = {
    "Lady Opal's Egg: Pool": None,

    "Shroom: Prismic Palace - Pool 1": None,
    "Shroom: Prismic Palace - Pool 2": None,
    "Shroom: Prismic Palace - Pool 3": None,
    "Shroom: Prismic Palace - Pool 4": None,
    "Shroom: Prismic Palace - Pool 5": None
  }

  r.region_connections = {
    Main: None,
    PoolCardLedge: Any(
      event.Collected("Unfreeze Prismic Palace") & Any(
        carrying.bubble_conch, carrying.shelnerts_fish,
        item.sprint & item.double_jump
      ),

      # launch from the tiny dive hole
      item.sprint & item.double_jump & item.wings,
      (carrying.bubble_conch | carrying.shelnerts_fish) & Any(
        item.wings,
        tech.bubble_jump,
      ),
    )
  }

@lazy_region
def PoolCardLedge(r: Region):
  r.locations = {
    "Card: Prismic Palace - Above Pool": None
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def EntrancePomLedge(r: Region):
  r.locations = {
    "Shroom: Prismic Palace - Entry Tree 1": None,
    "Shroom: Prismic Palace - Entry Tree 2": None,
    "Shroom: Prismic Palace - Entry Tree 3": None,
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def PokiPokiCave(r: Region):
  r.locations = {
    "Shroom: Prismic Palace - Poms 1": None,
    "Shroom: Prismic Palace - Poms 2": None,
    "Shroom: Prismic Palace - Poms 3": None,
    "Shroom: Prismic Palace - Poms 4": None,
    "Shroom: Prismic Palace - Poms 5": None,

    "Lady Opal's Egg: Poki-Poki": Any(
      carrying.jester_boots,
      CanAirSwim,
      tech.wing_jump & tech.bubble_jump_and_recoil & tech.z_target,
      carrying.mr_kerringtons_wings & Any(
        tech.wing_jump,
        item.sprint,
        item.double_jump,
        item.high_jump,
      ),
      tech.any_super_jump,
      item.climb & Any(
        item.wings,
        tech.bubble_jump,
        item.double_jump
      ),
      item.double_jump & Any(
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump & item.high_jump
      )
    )
  }

  r.region_connections = {
    Main: None,
    Spires: None
  }

@lazy_region
def JesterBootsCove(r: Region):
  r.locations = {
    "Card: Prismic Palace - Snowcastle": None,
    "Egg: Prismic Palace - Snowcastle": event.Collected("Open Prismic Palace Snowcastle")
  }

  r.region_connections = {
    LostleafEntryway: Any(
      event.Collected("Open Palace-Lostleaf Connector"),
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      tech.any_super_jump,
      item.double_jump & Any(
        item.wings,
        item.high_jump,
        tech.ground_tail_jump,
        tech.air_tail_jump,
        item.horn
      ),
      item.high_jump & tech.ground_tail_jump & tech.z_target
    ),

    JesterBootsCoveDryJBRemovalField: Any(
      carrying.jester_boots,
      templates.high_jump_obstacle,
      item.climb,
      tech.wing_jump & tech.bubble_jump_and_recoil
    ),

    JesterBootsCoveUnderwater: event.Collected("Unfreeze Prismic Palace")
  }

@lazy_region
def JesterBootsCoveUnderwater(r: Region):
  r.locations = {
    UnstuckBigstar: item.horn
  }

  r.region_connections = {
    JesterBootsCove: event.Collected("Unfreeze Prismic Palace"),
    UpperWater: carrying.no_jester_boots,
    JesterBootsCoveLowerPlatforms: event.Collected("Unfreeze Prismic Palace") & Any(
      item.sprint,
      carrying.bubble_conch,
      carrying.shelnerts_fish,
    ),
    JesterBootsCoveFloatingPoms: event.Collected("Unfreeze Prismic Palace") & carrying.bubble_conch,
    LowerWater: Any(
      event.Collected("Open Palace-Lostleaf Connector"),
      event.Collected(UnstuckBigstar)
    )
  }

@lazy_region
def EnterLostleaf(r: Region):
  from ..LAKE import LostleafLake

  r.entrances = [
    LostleafDoor.define(
      LostleafLake.ValleyDoor,
      rule = carrying.no_jester_boots
    )
  ]

  r.region_connections = {
    LostleafEntryway: carrying.no_jester_boots
  }


@lazy_region
def LostleafEntryway(r: Region):
  r.locations = {
    AirSwimFromLostleafEntryway: carrying.no_jester_boots & item.swim & item.air_swim & tech.momentum_cancel
  }

  r.region_connections = {
    EnterLostleaf: None,
    JesterBootsCove: Any(
      event.Collected("Open Palace-Lostleaf Connector"),
      carrying.no_jester_boots & Any(
        event.Collected(AirSwimFromLostleafEntryway),
        item.roll & item.sprint & item.high_jump & difficulty.intermediate,
        tech.any_super_jump,
        item.double_jump & Any(
          item.wings,
          item.high_jump,
          tech.ground_tail_jump,
          tech.air_tail_jump,
          item.horn
        ),
        item.high_jump & tech.ground_tail_jump & tech.z_target
      ),
    )
  }

@lazy_region
def JesterBootsCoveLowerPlatforms(r: Region):
  r.locations = {
    "Shroom: Prismic Palace - Jester Boots 1": None,
    "Shroom: Prismic Palace - Jester Boots 2": None,
    "Shroom: Prismic Palace - Jester Boots 3": None,
    "Shroom: Prismic Palace - Jester Boots 4": None,
  }

  r.region_connections = {
    JesterBootsCove: None,
    Main: carrying.no_jester_boots,
    JesterBootsCoveCastlePlatform: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings & tech.wing_jump,

      templates.high_jump_obstacle,

      tech.wing_jump & tech.bubble_jump_and_recoil & tech.z_target
    ),
    JesterBootsCoveLowerCastle: Any(
      item.wings,
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      tech.bubble_jump
    ),
    LostleafEntryway: Any(
      item.air_tail & item.roll & tech.bubble_jump
    ),
    JesterBootsCoveFloatingPoms: tech.any_super_jump
  }

@lazy_region
def JesterBootsCoveCastlePlatform(r: Region):
  r.locations = {
    "Shroom: Prismic Palace - Jester Boots 5": None
  }

  r.region_connections = {
    JesterBootsCoveLowerPlatforms: None,
    JesterBootsCoveLowerCastle: None,
    JesterBootsCoveMidCastle: None
  }

@lazy_region
def JesterBootsCoveLowerCastle(r: Region):
  r.locations = {
    ValleyJesterBoots: None
  }

  r.region_connections = {
    JesterBootsCove: None,
    LostleafEntryway: carrying.jester_boots | carrying.mr_kerringtons_wings
  }

@lazy_region
def JesterBootsCoveMidCastle(r: Region):
  r.region_connections = {
    JesterBootsCoveUpperCastle: Any(
      carrying.jester_boots,
      Comment(
        "Perform a coyote-time jump after climbing up one of the spires",
        difficulty.intermediate,
      ),
      templates.high_jump_obstacle
    ),
    LostleafEntryway: item.wings,
    JesterBootsCoveLowerCastle: None,
    JesterBootsCoveCastlePlatform: None,
    JesterBootsCove: None
  }

@lazy_region
def JesterBootsCoveUpperCastle(r: Region):
  r.region_connections = {
    JesterBootsCoveLowerCastle: None,
    JesterBootsCoveFloatingPoms: Any(
      carrying.jester_boots,
      tech.wing_jump & tech.bubble_jump_and_recoil & tech.z_target,
      carrying.mr_kerringtons_wings & tech.wing_jump,
      item.air_tail & item.roll & tech.bubble_jump
    )
  }

@lazy_region
def JesterBootsCoveFloatingPoms(r: Region):
  r.region_connections = {
    JesterBootsCove: None,
    OuterRim: carrying.jester_boots & item.roll & tech.ejection_launch,
    JesterBootsCovePrestonPlatform: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      item.wings & item.horn,
      (tech.bubble_jump | item.wings) & Any(
        tech.ground_tail_jump,
        tech.air_tail_jump,
        item.double_jump
      ),
      tech.wing_jump,
      item.air_tail & item.roll,
    )
  }

@lazy_region
def JesterBootsCovePrestonPlatform(r: Region):
  r.locations = {
    "Prismic Palace - Snowcastle Preston": None
  }

  r.region_connections = {
    JesterBootsCove: None,
    JesterBootsCoveFloatingPoms: None
  }

@lazy_region
def Spires(r: Region):
  r.locations = {
    "Shroom: Prismic Palace - Pom Spire 1": None,
    "Shroom: Prismic Palace - Pom Spire 2": None,
    "Shroom: Prismic Palace - Pom Spire 3": None,
    "Shroom: Prismic Palace - Pom Spire 4": None,
    "Shroom: Prismic Palace - Pom Spire 5": None,

    "Shroom: Prismic Palace - Observatory Spire 1": None,
    "Shroom: Prismic Palace - Observatory Spire 2": None,
    "Shroom: Prismic Palace - Observatory Spire 3": None,
    "Shroom: Prismic Palace - Observatory Spire 4": None,
    "Shroom: Prismic Palace - Observatory Spire 5": None,

    "Lady Opal's Egg: Castle": None,
  }

  from . import DiningRoom

  r.entrances = [
    DiningRoomDoor.define(DiningRoom.ValleyDoor)
  ]

  r.region_connections = {
    Main: None,
    PokiPokiCave: templates.high_jump_obstacle,
    ObservatoryPlatform: Any(
      item.horn,
      item.double_jump,
      item.high_jump,
      tech.ground_tail_jump,
      tech.air_tail_jump,
    )
  }

@lazy_region
def ObservatoryEntry(r: Region):
  from . import Observatory

  r.entrances = [
    ObservatoryDoor.define(Observatory.ValleyDoor)
  ]

  r.region_connections = {
    ObservatoryPlatform: None
  }

@lazy_region
def ObservatoryPlatform(r: Region):
  r.locations = {
    "Shroom: Prismic Palace - Observatory Slide 1": None,
    "Shroom: Prismic Palace - Observatory Slide 2": None,
    "Shroom: Prismic Palace - Observatory Slide 3": None,
    "Shroom: Prismic Palace - Observatory Slide 4": None,
    "Shroom: Prismic Palace - Observatory Slide 5": None,

    "Prismic Palace - Observatory Preston": None
  }

  r.entrances = [
    ObservatoryShortcutDoorTop.define(
      default_connection = ObservatoryShortcutDoorBottom,
      rule = event.Collected("Open Observatory Shortcut")
    )
  ]

  r.region_connections = {
    ObservatoryEntry: event.Collected("Unfreeze Prismic Palace"),

    ObservatoryRoof: Any(
      templates.high_jump_obstacle
    ),

    ObservatorySlideEnd: Any(
      carrying.mr_kerringtons_wings,
      item.roll & Any(
        tech.bubble_jump,
        item.sprint,
        item.wings
      )
    ),

    OuterRim: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      tech.super_bounce & tech.momentum_cancel,
      tech.super_bubble_jump,
      item.wings & item.double_jump,
      item.sprint & Any(
        item.double_jump & tech.bubble_jump,
      ),
      item.roll & (item.air_tail | item.sprint) & Any(
        tech.bubble_jump,
        item.double_jump,
        item.wings
      )
    )
  }

@lazy_region
def ObservatoryRoof(r: Region):
  r.locations = {
    "Card: Prismic Palace - Top of Observatory": None
  }

  r.region_connections = {
    ObservatoryPlatform: None,
    ObservatoryEntry:
      tech.roll_disjoint & (item.air_tail | item.ground_tail),
    ObservatorySlideEnd: item.wings,
    OuterRim: Any(
      item.wings,
      tech.bubble_jump & item.double_jump
    )
  }

@lazy_region
def ObservatorySlideEnd(r: Region):
  r.locations = {
    "Egg: Prismic Palace - Observatory Slide": None
  }

  r.region_connections = {
    ObservatoryPlatform: None
  }

@lazy_region
def OuterRim(r: Region):
  r.region_connections = {
    Main: None,
    JesterBootsCoveFloatingPoms: None,
    JesterBootsCoveUpperCastle: None,
    EntrancePomLedge: None,
    PalaceCardLedge: None,
    PokiPokiCave: None,
    ObservatoryPlatform: Any(
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
      item.sprint & item.roll,
      item.wings,
    ),
    PalaceTop: Any(
      tech.super_bounce & Any(
        difficulty.hard,
        item.wings,
        tech.bubble_jump
      ),
      tech.super_bubble_jump
    )
  }

@lazy_region
def PalaceCardLedge(r: Region):
  r.locations = {
    "Card: Prismic Palace - Top of Palace": None
  }

  r.region_connections = {
    Main: None,
    OuterRim: Any(
      tech.any_super_jump,
      tech.bubble_jump,
      item.wings,
      item.double_jump & Any(
        tech.ground_tail_jump,
        tech.air_tail_jump
      ),
      tech.air_tail_jump & tech.momentum_cancel,
      item.air_tail & item.roll,
      item.sprint & item.double_jump
    ),
    Spires: None,
    PokiPokiCave: None
  }

@lazy_region
def PalaceTop(r: Region):
  r.locations = {
    "Egg: Prismic Palace - Top of the Palace": None
  }

  from . import Sanctum

  r.entrances = [
    SanctumDoor.define(Sanctum.ValleyDoor)
  ]

  r.region_connections = {
    OuterRim: Any(
      item.wings,
      item.double_jump,
      item.sprint,
      tech.bubble_jump
    )
  }

@lazy_region
def ClipIntoIce(r: Region):
  r.region_connections = {
    PalaceTop: tech.ejection_launch,
    OuterRim: tech.ejection_launch,
    UpperWater: None
  }

@lazy_region
def UpperWater(r: Region):
  r.locations = {
    "Shroom: Prismic Palace - Lake Corner 1": None,
    "Shroom: Prismic Palace - Lake Corner 2": None,
    "Shroom: Prismic Palace - Lake Corner 3": None,

    "Shroom: Prismic Palace - Lake Plants 1": None,
    "Shroom: Prismic Palace - Lake Plants 2": None,
    "Shroom: Prismic Palace - Lake Plants 3": None,
    "Shroom: Prismic Palace - Lake Plants 4": None,
    "Shroom: Prismic Palace - Lake Plants 5": None,
    "Shroom: Prismic Palace - Lake Plants 6": None,

    "Shroom: Prismic Palace - Lake Behind 1": None,
    "Shroom: Prismic Palace - Lake Behind 2": None,
    "Shroom: Prismic Palace - Lake Behind 3": None,

    "Shroom: Prismic Palace - Lake Gobbler 1": None,
    "Shroom: Prismic Palace - Lake Gobbler 2": None,
    "Shroom: Prismic Palace - Lake Gobbler 3": None,

    "Prismic Palace - Feed Gobbler": carrying.apple,

    "Prismic Palace - Angel Statue Puzzle": Any(
      item.ground_tail, item.air_tail,
      carrying.apple, carrying.bubble_conch
    ),
  }

  from . import Palace

  r.entrances = [
    PalaceFrontDoor.define(
      default_connection = Palace.FrontDoor,
      rule = Any(
        event.Collected("Open Prismic Palace Gate"),
        tech.roll_disjoint
      )
    )
  ]

  r.region_connections = {
    Main: event.Collected("Unfreeze Prismic Palace"),
    GobblerCave: event.Collected("Snooze Gobbler"),
    JesterBootsCoveUnderwater: carrying.no_jester_boots,
    BreakLowerWaterWall: Any(
      item.roll & Any(
        item.ground_tail,
        item.air_tail
      ),
      item.horn,
      carrying.apple, carrying.bubble_conch
    ),
    LowerWater: Any(
      event.Collected(BrokeLowerWaterWall),
    )
  }

@lazy_region
def BigstarCave(r: Region):
  r.locations = {
    "Egg: Prismic Palace - Bigstar": None,
    "Prismic Palace - Bigstar Preston": None
  }

  r.region_connections = {
    UpperWater: event.Collected(UnstuckBigstar),
    LowerWater: event.Collected("Open Bigstar Cave")
  }

@lazy_region
def LowerWater(r: Region):
  r.locations = {
    "Palace-Lostleaf Connector - Preston": None,

    "Shroom: Prismic Palace - Lake Basement Entry 1": None,
    "Shroom: Prismic Palace - Lake Basement Entry 2": None,
    "Shroom: Prismic Palace - Lake Basement Entry 3": None,
    "Shroom: Prismic Palace - Lake Basement Entry 4": None,
    "Shroom: Prismic Palace - Lake Basement Entry 5": None,
    "Shroom: Prismic Palace - Lake Basement Entry 6": None,
    "Shroom: Prismic Palace - Lake Basement Entry 7": None,
    "Shroom: Prismic Palace - Lake Basement Entry 8": None,

    "Shroom: Prismic Palace - Lake Mushroom Cave 1": None,
    "Shroom: Prismic Palace - Lake Mushroom Cave 2": None,
    "Shroom: Prismic Palace - Lake Mushroom Cave 3": None,
    "Shroom: Prismic Palace - Lake Mushroom Cave 4": None,
    "Shroom: Prismic Palace - Lake Mushroom Cave 5": None,

    "Shroom: Prismic Palace - Lake Basement Overpass 1": None,
    "Shroom: Prismic Palace - Lake Basement Overpass 2": None,
    "Shroom: Prismic Palace - Lake Basement Overpass 3": None,
    "Shroom: Prismic Palace - Lake Basement Overpass 4": None,
    "Shroom: Prismic Palace - Lake Basement Overpass 5": None,

    "Prismic Palace - Basement Star Hoops": None,
  }

  from . import Palace

  r.entrances = [
    PalaceBasementDoor.define(
      default_connection = Palace.BasementDoor,
      rule = event.Collected("Open Prismic Palace Basement")
    )
  ]

  r.region_connections = {
    UpperWater: Any(
      event.Collected(BrokeLowerWaterWall),
    ),

    JesterBootsCoveUnderwater: Any(
      event.Collected("Open Palace-Lostleaf Connector"),
      event.Collected(UnstuckBigstar)
    ),

    BigstarCave: event.Collected("Open Bigstar Cave"),

    GobblerCave: event.Collected("Open Gobbler Cave"),

    BreakLowerWaterWall: Any(
      item.air_tail, item.ground_tail,
      carrying.apple, carrying.bubble_conch
    )
  }

@lazy_region
def BreakLowerWaterWall(r: Region):
  r.locations = {
    BrokeLowerWaterWall: None
  }

@lazy_region
def GobblerCave(r: Region):
  r.locations = {
    "Egg: Prismic Palace - Gobbler": None,
    "Prismic Palace - Gobbler Preston": None
  }

  r.region_connections = {
    UpperWater: event.Collected("Snooze Gobbler"),
    LowerWater: event.Collected("Open Gobbler Cave")
  }
