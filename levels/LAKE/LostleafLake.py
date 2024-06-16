from ...logic import Region, Entrance, Any
from ...logic import AppleTreeLocation
from ...logic.comment import Comment
from ...logic.whackable import Whackable
from ...logic import item, difficulty, tech, carrying

class Main(Region): pass
class RingBell(Region): pass
class BellTower(Region): pass
class OuterRim(Region): pass
class LobbyEntry(Region): pass

class LostleafLobbyDoor(Entrance): pass
class DucklingsDoorUpper(Entrance): pass
class DucklingsDoorLower(Entrance): pass

from ..CAVE import LostleafLobby

regions = [
  Main.define(
    locations = {
      AppleTreeLocation: item.carry & Any(
        Comment(
          "Grab the apple near the Winky Tree",
          difficulty.intermediate
        ),
        Whackable(
          horn_works = True,
          air_tail_works = True,
          ground_tail_works = True,
          roll_works = True,
          throwable_works = True
        )
      )
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

        Comment(
          "Climb the ladder",
          Any(
            carrying.plant_and_climb_tree,
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
      
      RingBell: Whackable(
        ground_tail_works = True,
        air_tail_works = True,
        roll_works = True,
        throwable_works = True,
        horn_works = True
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
