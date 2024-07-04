from typing import override
from ...logic.objects import EntranceType, PlantableSoil
from ...logic import Region, Entrance, Any
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

class Main(Region):
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
  }

  @override
  @classmethod
  def load(cls):
    from ..CAVE import LostleafLobby

    cls.entrances = [
      LostleafLobbyDoor.define(LostleafLobby.LostleafLakeDoor)
    ]

    cls.region_connections = {
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

class WaterfallEggCave(Region):
  locations = {
    "Egg: Lostleaf Lake - Waterfall": None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None
    }

class RingBell(Region):
  locations = {
    "Lostleaf Lake - Ring Bell": None
  }

  @override
  @classmethod
  def load(cls): pass

class BellTower(Region):
  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
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

class OuterRim(Region):
  @override
  @classmethod
  def load(cls):
    from ..CAVE import PrismicOutside

    cls.entrances = [
      PrismicDoor.define(
        default_connection = PrismicOutside.LostleafDoor
      )
    ]

    cls.region_connections = {
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

class SecretWorld(Region):
  @override
  @classmethod
  def load(cls):
    # NOTE: this SW implies swim

    cls.region_connections = {
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

class DeepWoods(Region):
  locations = {
    "Lostleaf Lake - Tree Puzzle": Any(
      item.ground_tail,
      item.air_tail,
      carrying.apple | carrying.bubble_conch,
    ),
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: event.Collected("Open Deep Woods"),

      DeepWoodsPuzzleEgg: event.Collected("Lower Deep Woods Egg"),

      DeepDeepWoods: carrying.no_jester_boots
    }

class DeepDeepWoods(Region):
  locations = {
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

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      DeepWoods: carrying.no_jester_boots
    }

class Lake(Region):
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
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
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

class LakeStump(Region):
  locations = {
    "Card: Lostleaf Lake - Lake Stump": None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
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

class InsideChurch(Region):
  @override
  @classmethod
  def load(cls):
    from . import Church

    cls.entrances = [
      ChurchDoor.define(
        default_connection = Church.LostleafLakeDoor,
        type = EntranceType.BILINEAR | EntranceType.UNDERWATER
      )
    ]

    cls.region_connections = {
      Lake: item.swim
    }

class InsideCrypt(Region):
  @override
  @classmethod
  def load(cls):
    from . import Crypt

    cls.entrances = [
      CryptDoor.define(
        default_connection = Crypt.LostleafLakeDoorFront
      )
    ]

    cls.region_connections = {
      TeepeeIsland: event.Collected("Open Crypt")
    }

class TeepeeIsland(Region):
  locations = {
    "Shroom: Lostleaf Lake - Teepee 1": None,
    "Shroom: Lostleaf Lake - Teepee 2": None,
    "Shroom: Lostleaf Lake - Teepee 3": None,

    "Card: Lostleaf Lake - Teepee": None,
  }

  @override
  @classmethod
  def load(cls):
    from . import Teepee

    cls.entrances = [
      TeepeeFrontDoor.define(Teepee.FrontDoor),
    ]

    cls.region_connections = {
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

class FallIntoTeepee(Region):
  @override
  @classmethod
  def load(cls):
    from . import Teepee

    cls.entrances = [
      TeepeeTopside.define(
        default_connection = Teepee.Topside,
        type = EntranceType.EXIT
      )
    ]

class PrestonLedge(Region):
  locations = {
    "Lostleaf Lake - Treehouse Preston": None,
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
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

class TreehouseBranches(Region):
  locations = {
    "Shroom: Lostleaf Lake - Treehouse Branches 1": None,
    "Shroom: Lostleaf Lake - Treehouse Branches 2": None,
    "Shroom: Lostleaf Lake - Treehouse Branches 3": None,
    "Shroom: Lostleaf Lake - Treehouse Branches 4": None,
    "Shroom: Lostleaf Lake - Treehouse Branches 5": None,
    "Shroom: Lostleaf Lake - Treehouse Branches 6": None,
    "Egg: Lostleaf Lake - Near the Treehouse": None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
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

class WinkyTreeLedge(Region):
  locations = {
    "Shroom: Lostleaf Lake - Winky Apple Tree 1": None,
    "Shroom: Lostleaf Lake - Winky Apple Tree 2": None,
    "Shroom: Lostleaf Lake - Winky Apple Tree 3": None,
    "Shroom: Lostleaf Lake - Winky Apple Tree 4": None,
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
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

class BigAppleLedge(Region):
  locations = {
    BigAppleLedgeSoil: carrying.apple
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
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

class TreehouseFrontEntry(Region):
  @override
  @classmethod
  def load(cls):
    from . import Treehouse

    cls.entrances = [
      TreehouseFrontDoor.define(
        default_connection = Treehouse.LostleafFrontDoor,
        rule = Any(
          event.Collected("Open Treehouse"),
          tech.roll_disjoint
        )
      )
    ]

    cls.region_connections = {
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

class TreehouseBackEntry(Region):
  @override
  @classmethod
  def load(cls):
    from . import Treehouse

    cls.entrances = [
      TreehouseBackDoor.define(
        default_connection = Treehouse.LostleafBackDoor
      )
    ]

    cls.region_connections = {
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

class TreehouseRoof(Region):
  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      TreehouseFrontEntry: None,

      TreehouseBackEntry: None,

      BigAppleLedge: Any(
        item.wings,
        carrying.mr_kerringtons_wings,
        carrying.jester_boots
      )
    }

class Ducklings(Region):
  @override
  @classmethod
  def load(cls):
    from ..CAVE import SunCavern

    cls.entrances = [
      DucklingsDoorUpper.define(SunCavern.DucklingsDoorUpper),
      DucklingsDoorLower.define(SunCavern.DucklingsDoorLower)
    ]

    cls.region_connections = {
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

class DucklingsLedge(Region):
  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
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

class CryptCanopy(Region):
  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      BigAppleLedge: None,
      OuterRim: None,
    }

class WaterfallCanopy(Region):
  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
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

class DeepWoodsPuzzleEgg(Region):
  locations = {
    "Egg: Lostleaf Lake - Deep Woods Puzzle": None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      DeepWoods: None
    }
