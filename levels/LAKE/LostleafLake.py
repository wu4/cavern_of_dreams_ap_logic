from ...logic.objects import EntranceType, PlantableSoil
from ...logic import lazy_region, Region, Entrance, Any
from ...logic.objects import CarryableLocation
from ...logic.comment import Comment
from ...logic import item, difficulty, tech, carrying, event, has, templates

class LostleafLobbyDoor(Entrance): pass
class DucklingsDoorUpper(Entrance): pass
class DucklingsDoorLower(Entrance): pass
class ChurchDoor(Entrance): pass
class CryptDoor(Entrance): pass
class PrismicDoor(Entrance): pass
class TreehouseFrontDoor(Entrance): pass
class TreehouseBackDoor(Entrance): pass
class TeepeeFrontDoor(Entrance): pass
class TeepeeTopside(Entrance): pass

class BellTowerSoil(PlantableSoil): pass
class WinkyTreeSoil(PlantableSoil): pass
class DeepDeepWoodsSoil(PlantableSoil): pass
class BigAppleLedgeSoil(PlantableSoil): pass

class LakeAppleTree(CarryableLocation): carryable = "Apple"
class DeepDeepWoodsAppleTree(CarryableLocation): carryable = "Apple"
class DeepDeepWoodsJesterBoots(CarryableLocation): carryable = "Jester Boots"

@lazy_region
def Main(r: Region):
  r.locations = {
    LakeAppleTree: item.carry & Any(
      Comment(
        "Grab the apple near the Winky Tree",
        difficulty.intermediate
      ),
      item.horn,
      item.air_tail,
      item.ground_tail,
      carrying.apple | carrying.bubble_conch
    ),

    WinkyTreeSoil: carrying.apple,

    BellTowerSoil: carrying.apple,

    "Lostleaf Lake - Winky Tree Target": Any(
      carrying.apple | carrying.bubble_conch,
      tech.ground_tail_jump,
      item.air_tail & Any(
        carrying.jester_boots,
        tech.air_tail_jump,
        item.horn,
        item.high_jump,
      ),
      item.double_jump & item.horn
    ),

    "Lostleaf Lake - Help Shelnert": has.Collected("Fish Food"),

    "Egg: Lostleaf Lake - Entry Stump": None,

    "Card: Lostleaf Lake - Entry": None,
    "Card: Lostleaf Lake - Apple Tree": None,

    "Shroom: Lostleaf Lake - Lake Logs 1": None,
    "Shroom: Lostleaf Lake - Lake Logs 2": None,
    "Shroom: Lostleaf Lake - Lake Logs 3": None,
    "Shroom: Lostleaf Lake - Lake Logs 4": None,

    "Shroom: Lostleaf Lake - Bridge 1": None,
    "Shroom: Lostleaf Lake - Bridge 2": None,
    "Shroom: Lostleaf Lake - Bridge 3": None,

    "Shroom: Lostleaf Lake - Winky Apple Tree 1": None,
    "Shroom: Lostleaf Lake - Winky Apple Tree 2": None,
    "Shroom: Lostleaf Lake - Winky Apple Tree 3": None,
    "Shroom: Lostleaf Lake - Winky Apple Tree 4": None,

    "Shroom: Lostleaf Lake - Ramp to Winky Tree 1": None,
    "Shroom: Lostleaf Lake - Ramp to Winky Tree 2": None,
    "Shroom: Lostleaf Lake - Ramp to Winky Tree 3": None,
    "Shroom: Lostleaf Lake - Ramp to Winky Tree 4": None,
    "Shroom: Lostleaf Lake - Ramp to Winky Tree 5": None,

    "Shroom: Lostleaf Lake - Deep Woods Entryway 1": None,
    "Shroom: Lostleaf Lake - Deep Woods Entryway 2": None,
    "Shroom: Lostleaf Lake - Deep Woods Entryway 3": None,

    "Shroom: Lostleaf Lake - Waterfall Logs 1": None,
    "Shroom: Lostleaf Lake - Waterfall Logs 2": None,
    "Shroom: Lostleaf Lake - Waterfall Logs 3": None,
    "Shroom: Lostleaf Lake - Waterfall Logs 4": None,

    "Shroom: Lostleaf Lake - Winky Bouncy Mushroom 1": None,
    "Shroom: Lostleaf Lake - Winky Bouncy Mushroom 2": None,
    "Shroom: Lostleaf Lake - Winky Bouncy Mushroom 3": None
  }

  from ..CAVE import LostleafLobby

  r.entrances = [
    LostleafLobbyDoor.define(LostleafLobby.LostleafLakeDoor)
  ]

  r.region_connections = {
    OuterRim: Any(
      tech.any_super_jump,

      item.roll & item.air_tail & tech.ability_toggle & item.double_jump,

      tech.ground_tail_jump & item.high_jump & item.double_jump & item.wings,

      item.swim & item.air_swim & tech.momentum_cancel
    ),

    Lake: item.swim,

    LakeStump: Any(
      difficulty.intermediate & Any(
        item.horn
      ),

      Comment(
        "Come from above",
        Any(
          carrying.mr_kerringtons_wings,
          item.wings,
          item.air_tail,
          tech.bubble_jump,
          item.sprint
        )
      ),

      item.double_jump,
      tech.ground_tail_jump,
    ),

    WaterfallEggCave: Any(
      item.ground_tail,
      item.air_tail,
      carrying.apple | carrying.bubble_conch
    ),

    DeepWoods: event.Collected("Open Deep Woods"),

    BellTower: Any(
      tech.any_super_jump,

      event.Collected(BellTowerSoil) & item.climb,
      Comment(
        "Climb the ladder",
        Any(
          item.climb & Any(
            tech.ground_tail_jump,
            tech.air_tail_jump & item.high_jump,
            item.double_jump,
            item.horn,
            Comment(
              "Launch from the side of the church",
              item.roll & item.air_tail
            )
          )
        )
      )
    ),

    RingBell: Any(
      Comment(
        "First-person snipe",
        item.bubble
      ),
      Comment(
        "Launch from the deep water and throw at a distance",
        item.swim & carrying.bubble_conch
      )
    ),

    TreehouseBranches: Any(
      event.Collected("Raise Lake Swings"),
      Comment(
        "Jump from the Winky Tree target",
        item.horn & item.double_jump
      )
    ),

    PrestonLedge: Any(
      tech.any_super_jump,

      event.Collected("Raise Lake Swings"),

      item.double_jump & Any(
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump & item.high_jump,
        event.Collected(WinkyTreeSoil) & item.climb
      )
    ),

    WinkyTreeLedge: Any(
      tech.any_super_jump,

      item.double_jump,
      item.high_jump & tech.air_tail_jump,
      tech.ground_tail_jump,
      item.horn
    ),
  }

@lazy_region
def WaterfallEggCave(r: Region):
  r.locations = {
    "Egg: Lostleaf Lake - Waterfall": None
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def RingBell(r: Region):
  r.locations = {
    "Lostleaf Lake - Ring Bell": None
  }

@lazy_region
def BellTower(r: Region):
  r.region_connections = {
    OuterRim: Any(
      tech.bubble_jump & Any(
        item.double_jump,
        tech.ground_tail_jump,
        tech.air_tail_jump
      ),
      item.wings & Any(
        tech.bubble_jump_and_recoil,
        item.horn,
        item.climb,
        item.double_jump,
        tech.ground_tail_jump,
        tech.air_tail_jump
      ),
      item.roll & item.air_tail
    ),

    RingBell: Any(
      item.ground_tail,
      item.air_tail,
      item.horn,
      carrying.apple | carrying.bubble_conch
    ),

    Main: None
  }

@lazy_region
def OuterRim(r: Region):
  from ..CAVE import PrismicOutside

  r.entrances = [
    PrismicDoor.define(
      default_connection = PrismicOutside.LostleafDoor
    )
  ]

  r.region_connections = {
    TeepeeIsland: None,
    Main: None,

    FallIntoTeepee: Any(
      carrying.mr_kerringtons_wings,
      tech.wing_storage,
      carrying.jester_boots
    ),

    PrestonLedge: Any(
      item.ground_tail,
      item.air_tail,
      carrying.apple | carrying.bubble_conch,

      carrying.jester_boots,

      Any(
        item.horn,
        tech.ground_tail_jump,
        tech.wing_jump,
        item.double_jump,
        difficulty.hard & item.high_jump
      ) & Any(
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump,
        item.wings,
        tech.bubble_jump,
      )
    ),

    BellTower: Any(
      tech.bubble_jump & Any(
        item.double_jump,
        tech.ground_tail_jump,
        tech.air_tail_jump
      ),
      item.wings & Any(
        tech.bubble_jump_and_recoil,
        item.horn,
        item.climb,
        item.double_jump,
        tech.ground_tail_jump,
        tech.air_tail_jump
      ),
      item.roll & (item.air_tail | item.sprint)
    )
  }

@lazy_region
def SecretWorld(r: Region):
  # NOTE: this SW implies swim

  r.region_connections = {
    Main: None,

    DucklingsLedge: tech.ejection_launch,
    WaterfallCanopy: tech.ejection_launch,
    BellTower: tech.ejection_launch,

    DeepWoods: Any(
      item.air_swim,
      difficulty.hard & item.double_jump & item.wings & item.sprint,
      carrying.jester_boots
    ),

    DeepDeepWoods: Any(
      item.air_swim,
      carrying.jester_boots
    ),

    InsideCrypt: None,

    BigAppleLedge: Any(
      item.wings,
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
      item.air_swim,
    ),

    InsideChurch: None,

    WaterfallEggCave: Any(
      item.air_swim,
      difficulty.hard & item.double_jump & item.sprint,
      carrying.jester_boots
    )
  }

@lazy_region
def DeepWoods(r: Region):
  r.locations = {
    "Lostleaf Lake - Tree Puzzle": Any(
      item.ground_tail,
      item.air_tail,
      carrying.apple | carrying.bubble_conch,
    ),
  }

  r.region_connections = {
    Main: event.Collected("Open Deep Woods"),

    DeepWoodsPuzzleEgg: event.Collected("Lower Deep Woods Egg"),

    DeepDeepWoods: carrying.no_jester_boots
  }

@lazy_region
def DeepDeepWoods(r: Region):
  r.locations = {
    "Shroom: Lostleaf Lake - Deep Woods 1": None,
    "Shroom: Lostleaf Lake - Deep Woods 2": None,
    "Shroom: Lostleaf Lake - Deep Woods 3": None,
    "Shroom: Lostleaf Lake - Deep Woods 4": None,
    "Shroom: Lostleaf Lake - Deep Woods 5": None,
    "Shroom: Lostleaf Lake - Deep Woods 6": None,

    DeepDeepWoodsJesterBoots: None,
    DeepDeepWoodsAppleTree: item.carry,

    DeepDeepWoodsSoil: carrying.apple,

    "Egg: Lostleaf Lake - Jester Boots": Any(
      event.Collected(DeepDeepWoodsSoil) & Any(
        templates.high_jump_obstacle,
      ),
      carrying.jester_boots,
    ),
  }

  r.region_connections = {
    DeepWoods: carrying.no_jester_boots
  }

@lazy_region
def Lake(r: Region):
  r.locations = {
    "Lostleaf Lake - Back of the Headstone": Any(
      item.air_tail,
      item.ground_tail,
      item.horn,
      carrying.apple | carrying.bubble_conch
    ),

    "Egg: Lostleaf Lake - Lake Log": None,

    "Shroom: Lostleaf Lake - Behind Church 1": None,
    "Shroom: Lostleaf Lake - Behind Church 2": None,
    "Shroom: Lostleaf Lake - Behind Church 3": None,

    "Shroom: Lostleaf Lake - Church Entryway 1": None,
    "Shroom: Lostleaf Lake - Church Entryway 2": None,
    "Shroom: Lostleaf Lake - Church Entryway 3": None,

    "Shroom: Lostleaf Lake - Lake Gravestone 1": None,
    "Shroom: Lostleaf Lake - Lake Gravestone 2": None,
    "Shroom: Lostleaf Lake - Lake Gravestone 3": None,
  }

  r.region_connections = {
    SecretWorld: Comment(
      "Use the tombstone fish to clip out of bounds",
      tech.out_of_bounds & carrying.no_throwables
    ),

    OuterRim: carrying.bubble_conch,

    Main: None,

    InsideChurch: Any(
      event.Collected("Open Church")
    ),

    TeepeeIsland: None,
  }

@lazy_region
def LakeStump(r: Region):
  r.locations = {
    "Card: Lostleaf Lake - Lake Stump": None
  }

  r.region_connections = {
    Main: None,

    TeepeeIsland: Any(
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
      tech.super_bubble_jump,

      item.wings & Any(
        tech.super_bounce,
        item.double_jump,
        item.horn
      ),

      Comment(
        "Aim for the fence and repeatedly ledgegrab to get around",
        difficulty.intermediate & Any(
          tech.bubble_jump & Any(
            item.double_jump,

            tech.momentum_cancel & Any(
              item.horn,
              tech.air_tail_jump,
              tech.ground_tail_jump
            )
          ),

          item.wings,

          difficulty.hard & Any(
            item.air_tail & item.roll,
            tech.super_bounce & item.air_tail
          )
        )
      )
    )
  }

@lazy_region
def InsideChurch(r: Region):
  from . import Church

  r.entrances = [
    ChurchDoor.define(
      default_connection = Church.LostleafLakeDoor,
      type = EntranceType.BILINEAR | EntranceType.UNDERWATER
    )
  ]

  r.region_connections = {
    Lake: item.swim
  }

@lazy_region
def InsideCrypt(r: Region):
  from . import Crypt

  r.entrances = [
    CryptDoor.define(
      default_connection = Crypt.LostleafLakeDoorFront
    )
  ]

  r.region_connections = {
    TeepeeIsland: event.Collected("Open Crypt")
  }

@lazy_region
def TeepeeIsland(r: Region):
  r.locations = {
    "Shroom: Lostleaf Lake - Teepee 1": None,
    "Shroom: Lostleaf Lake - Teepee 2": None,
    "Shroom: Lostleaf Lake - Teepee 3": None,

    "Card: Lostleaf Lake - Teepee": None,
  }

  from . import Teepee

  r.entrances = [
    TeepeeFrontDoor.define(Teepee.FrontDoor),
  ]

  r.region_connections = {
    Lake: item.swim,

    FallIntoTeepee: Any(
      tech.any_super_jump,
      tech.ground_tail_jump & item.double_jump & item.high_jump & item.wings
    ),

    InsideCrypt: event.Collected("Open Crypt"),

    Main: Any(
      carrying.jester_boots,
      tech.super_bubble_jump,

      Comment(
        "Over the fence and around to the mud",
        Any(
          carrying.mr_kerringtons_wings,
          item.wings & Any(
            item.double_jump,
            tech.ground_tail_jump
          ),

          tech.bubble_jump & Any(
            item.air_tail & tech.z_target & Any(
              item.double_jump,
              tech.ground_tail_jump,
              item.horn
            ),

            tech.ground_tail_jump & item.double_jump,
          )
        )
      )
    ),

    OuterRim: Any(
      tech.any_super_jump,

      item.double_jump & item.wings & tech.ground_tail_jump & item.high_jump,

      tech.ejection_launch & Any(
        Comment(
          """
          Jump from the leaf pile for enough height to touch the top of the
          fence
          """,
          Any(
            difficulty.hard & item.sprint,
            difficulty.intermediate & tech.bubble_jump,
            carrying.jester_boots,
          )
        ),

        item.high_jump,
        item.double_jump,
        item.wings,
        carrying.mr_kerringtons_wings,
        item.horn,
        tech.air_tail_jump,
        tech.ground_tail_jump,
      )
    )
  }

@lazy_region
def FallIntoTeepee(r: Region):
  from . import Teepee

  r.entrances = [
    TeepeeTopside.define(
      default_connection = Teepee.Topside,
      type = EntranceType.EXIT
    )
  ]

@lazy_region
def PrestonLedge(r: Region):
  r.locations = {
    "Lostleaf Lake - Treehouse Preston": None,
  }

  r.region_connections = {
    Main: None,

    TreehouseBranches: Any(
      item.ground_tail,
      item.air_tail,

      item.high_jump,
      item.horn,
      item.double_jump,

      Comment(
        "Launch from the nearby fence",
        tech.ejection_launch
      )
    )
  }

@lazy_region
def TreehouseBranches(r: Region):
  r.locations = {
    "Shroom: Lostleaf Lake - Treehouse Branches 1": None,
    "Shroom: Lostleaf Lake - Treehouse Branches 2": None,
    "Shroom: Lostleaf Lake - Treehouse Branches 3": None,
    "Shroom: Lostleaf Lake - Treehouse Branches 4": None,
    "Shroom: Lostleaf Lake - Treehouse Branches 5": None,
    "Shroom: Lostleaf Lake - Treehouse Branches 6": None,
    "Egg: Lostleaf Lake - Near the Treehouse": None
  }

  r.region_connections = {
    Main: None,

    PrestonLedge: None,

    BigAppleLedge: Comment(
      "Jump onto the egg house",
      templates.high_jump_obstacle
    ),

    TreehouseFrontEntry: Any(
      item.climb,

      item.high_jump & carrying.mr_kerringtons_wings,

      item.wings & Any(
        item.double_jump,
        item.horn,
      ),

      item.double_jump & Any(
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump & item.high_jump,
      )
    ),
  }

@lazy_region
def WinkyTreeLedge(r: Region):
  r.locations = {
    "Shroom: Lostleaf Lake - Winky Apple Tree 1": None,
    "Shroom: Lostleaf Lake - Winky Apple Tree 2": None,
    "Shroom: Lostleaf Lake - Winky Apple Tree 3": None,
    "Shroom: Lostleaf Lake - Winky Apple Tree 4": None,
  }

  r.region_connections = {
    Main: None,

    BigAppleLedge: Any(
      tech.any_super_jump,

      item.high_jump & tech.ground_tail_jump,

      item.double_jump & Any(
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump,
        item.high_jump
      )
    )
  }

@lazy_region
def BigAppleLedge(r: Region):
  r.locations = {
    BigAppleLedgeSoil: carrying.apple
  }

  r.region_connections = {
    TreehouseBranches: None,

    WinkyTreeLedge: None,

    TreehouseFrontEntry: Any(
      carrying.mr_kerringtons_wings,

      item.wings & Any(
        item.sprint,
        tech.bubble_jump_and_recoil
      )
    ),

    WaterfallCanopy: tech.any_super_jump,

    CryptCanopy: Any(
      tech.any_super_jump,
      event.Collected(BigAppleLedgeSoil) & item.climb & item.double_jump & item.wings,
    )
  }

@lazy_region
def TreehouseFrontEntry(r: Region):
  from . import Treehouse

  r.entrances = [
    TreehouseFrontDoor.define(
      default_connection = Treehouse.LostleafFrontDoor,
      rule = Any(
        event.Collected("Open Treehouse"),
        tech.roll_disjoint
      )
    )
  ]

  r.region_connections = {
    TreehouseBranches: None,

    TreehouseBackEntry: carrying.jester_boots,

    TreehouseRoof: Any(
      tech.any_super_jump,

      Comment(
        "Launch from the ladder",
        tech.ejection_launch
      ),

      item.horn & item.double_jump & item.wings,

      difficulty.intermediate & Any(
        item.high_jump & tech.ground_tail_jump & item.double_jump,
      ),
    )
  }

@lazy_region
def TreehouseBackEntry(r: Region):
  from . import Treehouse

  r.entrances = [
    TreehouseBackDoor.define(
      default_connection = Treehouse.LostleafBackDoor
    )
  ]

  r.region_connections = {
    Main: None,

    TreehouseFrontEntry: carrying.jester_boots,

    BigAppleLedge: Any(
      carrying.jester_boots,
    ),

    TreehouseBranches: Any(
      item.wings,
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
    )
  }

@lazy_region
def TreehouseRoof(r: Region):
  r.region_connections = {
    TreehouseFrontEntry: None,

    TreehouseBackEntry: None,

    BigAppleLedge: Any(
      item.wings,
      carrying.mr_kerringtons_wings,
      carrying.jester_boots
    )
  }

@lazy_region
def Ducklings(r: Region):
  from ..CAVE import SunCavern

  r.entrances = [
    DucklingsDoorUpper.define(SunCavern.DucklingsDoorUpper),
    DucklingsDoorLower.define(SunCavern.DucklingsDoorLower)
  ]

  r.region_connections = {
    DucklingsLedge: Any(
      tech.any_super_jump,
      carrying.jester_boots,

      item.horn,
      item.wings & tech.bubble_jump_and_recoil,
      item.double_jump & Any(
        item.high_jump,
        tech.ground_tail_jump,
      )
    )
  }

@lazy_region
def DucklingsLedge(r: Region):
  r.region_connections = {
    Ducklings: None,
    TreehouseBranches: None,
    PrestonLedge: None,
    WaterfallCanopy: Any(
      tech.any_super_jump,
      tech.ejection_launch & Any(
        difficulty.hard,
        item.wings | tech.bubble_jump
      )
    )
  }

@lazy_region
def CryptCanopy(r: Region):
  r.region_connections = {
    BigAppleLedge: None,
    OuterRim: None,
  }

@lazy_region
def WaterfallCanopy(r: Region):
  r.region_connections = {
    DeepWoods: None,
    DeepWoodsPuzzleEgg: None,
    OuterRim: None,
    DucklingsLedge: None,
    Main: None,

    CryptCanopy: Any(
      item.wings,
      carrying.mr_kerringtons_wings,
      difficulty.hard & Any(
        item.roll & (item.air_tail | item.sprint) & item.double_jump
      ),
      item.roll & item.sprint & tech.bubble_jump,
    )
  }

@lazy_region
def DeepWoodsPuzzleEgg(r: Region):
  r.locations = {
    "Egg: Lostleaf Lake - Deep Woods Puzzle": None
  }

  r.region_connections = {
    DeepWoods: None
  }
