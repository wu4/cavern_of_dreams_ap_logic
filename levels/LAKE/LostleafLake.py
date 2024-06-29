from ...logic.objects import EntranceType, PlantableSoil
from ...logic import Region, Entrance, Any
from ...logic.objects import CarryableLocation
from ...logic.comment import Comment
from ...logic import item, difficulty, tech, carrying, event, has, templates

class Main(Region): pass
class RingBell(Region): pass
class BellTower(Region): pass
class OuterRim(Region): pass
class LobbyEntry(Region): pass
class SecretWorld(Region): pass
class DeepWoods(Region): pass
class WaterfallCave(Region): pass
class Lake(Region): pass
class LakeStump(Region): pass
class InsideChurch(Region): pass
class InsideCrypt(Region): pass
class TeepeeIsland(Region): pass
class PrestonLedge(Region): pass
class TreehouseBranches(Region): pass
class WinkyTreeLedge(Region): pass
class BigAppleLedge(Region): pass
class TreehouseFrontEntry(Region): pass
class TreehouseBackEntry(Region): pass
class TreehouseRoof(Region): pass
class Ducklings(Region): pass
class DucklingsLedge(Region): pass
class CryptCanopy(Region): pass
class WaterfallCanopy(Region): pass
class DeepWoodsPuzzleEgg(Region): pass

class Test:
  a = 1

class LostleafLobbyDoor(Entrance): pass
class DucklingsDoorUpper(Entrance): pass
class DucklingsDoorLower(Entrance): pass
class ChurchDoor(Entrance): pass
class CryptDoor(Entrance): pass
class PrismicDoor(Entrance): pass
class TreehouseFrontDoor(Entrance): pass
class TreehouseBackDoor(Entrance): pass

class BellTowerSoil(PlantableSoil): pass
class WinkyTreeSoil(PlantableSoil): pass
class DeepWoodsSoil(PlantableSoil): pass
class LakeAppleTree(CarryableLocation):
  carryable = "Apple"

class DeepWoodsAppleTree(CarryableLocation):
  carryable = "Apple"

class DeepWoodsJesterBoots(CarryableLocation):
  carryable = "Jester Boots"

from ..CAVE import LostleafLobby, SunCavern
from . import Church, Crypt, Treehouse
from ..PALACE import PrismicOutside

regions = [
  Main.define(
    locations = {
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
    },

    entrances = [
      LostleafLobbyDoor.define(LostleafLobby.LostleafLakeDoor)
    ],

    region_connections = {
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

      WaterfallCave: Any(
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
  ),

  LakeStump.define(
    locations = {
      "Card: Lostleaf Lake - Lake Stump": None
    },

    region_connections = {
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
  ),

  TeepeeIsland.define(
    locations = {
      "Shroom: Lostleaf Lake - Teepee 1": None,
      "Shroom: Lostleaf Lake - Teepee 2": None,
      "Shroom: Lostleaf Lake - Teepee 3": None,

      "Card: Lostleaf Lake - Teepee": None,
    },

    region_connections = {
      Lake: item.swim,

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
  ),

  Lake.define(
    locations = {
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
    },

    region_connections = {
      SecretWorld: Comment(
        "Use the tombstone fish to clip out of bounds",
        tech.out_of_bounds
      ),

      Main: None,

      InsideChurch: Any(
        event.Collected("Open Church")
      ),

      TeepeeIsland: None,
    }
  ),

  InsideChurch.define(
    entrances = [
      ChurchDoor.define(
        default_connection = Church.LostleafLakeDoor,
        type = EntranceType.BILINEAR | EntranceType.UNDERWATER
      )
    ],

    region_connections = {
      Lake: item.swim
    }
  ),

  InsideCrypt.define(
    entrances = [
      CryptDoor.define(
        default_connection = Crypt.LostleafLakeDoorFront
      )
    ],

    region_connections = {
      TeepeeIsland: event.Collected("Open Crypt")
    },
  ),

  BellTower.define(
    region_connections = {
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
  ),

  RingBell.define(
    locations = {
      "Lostleaf Lake - Ring Bell": None
    }
  ),

  OuterRim.define(
    entrances = [
      PrismicDoor.define(
        default_connection = PrismicOutside.LostleafDoor
      )
    ],

    region_connections = {
      TeepeeIsland: None,
      Main: None,

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
  ),

  PrestonLedge.define(
    locations = {
      "Lostleaf Lake - Treehouse Preston": None,
    },

    region_connections = {
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
  ),

  WinkyTreeLedge.define(
    locations = {
      "Shroom: Lostleaf Lake - Winky Apple Tree 1": None,
      "Shroom: Lostleaf Lake - Winky Apple Tree 2": None,
      "Shroom: Lostleaf Lake - Winky Apple Tree 3": None,
      "Shroom: Lostleaf Lake - Winky Apple Tree 4": None,
    },

    region_connections = {
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
  ),

  BigAppleLedge.define(
    region_connections = {
      TreehouseBranches: None,

      WinkyTreeLedge: None,

      TreehouseFrontEntry: Any(
        carrying.mr_kerringtons_wings,

        item.wings & Any(
          item.sprint,
          tech.bubble_jump_and_recoil
        )
      )
    }
  ),

  TreehouseBranches.define(
    locations = {
      "Shroom: Lostleaf Lake - Treehouse Branches 1": None,
      "Shroom: Lostleaf Lake - Treehouse Branches 2": None,
      "Shroom: Lostleaf Lake - Treehouse Branches 3": None,
      "Shroom: Lostleaf Lake - Treehouse Branches 4": None,
      "Shroom: Lostleaf Lake - Treehouse Branches 5": None,
      "Shroom: Lostleaf Lake - Treehouse Branches 6": None,
      "Egg: Lostleaf Lake - Near the Treehouse": None
    },

    region_connections = {
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
  ),

  TreehouseFrontEntry.define(
    entrances = [
      TreehouseFrontDoor.define(
        default_connection = Treehouse.LostleafFrontDoor,
        rule = Any(
          event.Collected("Open Treehouse"),
          tech.roll_disjoint
        )
      )
    ],

    region_connections = {
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
  ),

  TreehouseRoof.define(
    region_connections = {
      TreehouseFrontEntry: None,

      TreehouseBackEntry: None,

      BigAppleLedge: Any(
        item.wings,
        carrying.mr_kerringtons_wings,
        carrying.jester_boots
      )
    }
  ),

  TreehouseBackEntry.define(
    entrances = [
      TreehouseBackDoor.define(
        default_connection = Treehouse.LostleafBackDoor
      )
    ],

    region_connections = {
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
  ),

  Ducklings.define(
    entrances = [
      DucklingsDoorUpper.define(SunCavern.DucklingsDoorUpper),
      DucklingsDoorLower.define(SunCavern.DucklingsDoorLower)
    ],

    region_connections = {
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
  ),

  DucklingsLedge.define(
    region_connections = {
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
  ),

  DeepWoods.define(
    locations = {
      DeepWoodsJesterBoots: None,
      DeepWoodsAppleTree: item.carry,

      DeepWoodsSoil: carrying.apple,

      "Shroom: Lostleaf Lake - Deep Woods 1": None,
      "Shroom: Lostleaf Lake - Deep Woods 2": None,
      "Shroom: Lostleaf Lake - Deep Woods 3": None,
      "Shroom: Lostleaf Lake - Deep Woods 4": None,
      "Shroom: Lostleaf Lake - Deep Woods 5": None,
      "Shroom: Lostleaf Lake - Deep Woods 6": None,

      "Egg: Lostleaf Lake - Jester Boots": Any(
        event.Collected(DeepWoodsSoil) & Any(
          templates.high_jump_obstacle,
        ),
        carrying.jester_boots,
      ),

      "Lostleaf Lake - Tree Puzzle": Any(
        item.ground_tail,
        item.air_tail,
        carrying.apple | carrying.bubble_conch,
      ),
    },

    region_connections = {
      Main: event.Collected("Open Deep Woods"),
      DeepWoodsPuzzleEgg: event.Collected("Lower Deep Woods Egg")
    }
  ),

  DeepWoodsPuzzleEgg.define(
    locations = {
      "Egg: Lostleaf Lake - Deep Woods Puzzle": None
    },

    region_connections = {
      DeepWoods: None
    }
  ),

  WaterfallCanopy.define(
    region_connections = {
      DeepWoods: None,
      DeepWoodsPuzzleEgg: None,
      DucklingsLedge: None,
      Main: None,

      CryptCanopy: Any(
        item.wings,
        carrying.mr_kerringtons_wings
      )
    }
  )
]
