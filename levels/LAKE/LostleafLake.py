from ...logic.objects import PlantableSoil
from ...logic import Region, Entrance, Any
from ...logic.objects import CarryableLocation
from ...logic.comment import Comment
from ...logic import item, difficulty, tech, carrying, event, has

class Main(Region): pass
class RingBell(Region): pass
class BellTower(Region): pass
class OuterRim(Region): pass
class LobbyEntry(Region): pass

class LostleafLobbyDoor(Entrance): pass
class DucklingsDoorUpper(Entrance): pass
class DucklingsDoorLower(Entrance): pass

class BellTowerSoil(PlantableSoil): pass
class LakeAppleTree(CarryableLocation):
  carryable = "Apple"

from ..CAVE import LostleafLobby

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

      BellTowerSoil: carrying.apple,

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

        tech.ground_tail_jump & item.high_jump & item.double_jump & item.wings
      ),

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
      )
    }
  ),

  BellTower.define(
    region_connections = {
      OuterRim: Any(
        item.wings,
        item.air_tail & item.roll
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
    },

    region_connections = {
      Main: None
    }
  )
]
