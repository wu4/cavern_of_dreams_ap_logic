from ...logic import *

class Main(Region): pass
class RingBell(Region): pass
class BellTower(Region): pass
class OuterRim(Region): pass
class LobbyEntry(Region): pass

class LostleafLobbyDoor(Entrance): pass
class DucklingsDoorUpper(Entrance): pass
class DucklingsDoorLower(Entrance): pass

from ..CAVE import LostleafLobby as _LostleafLobby

regions = [
  Main.define(
    locations = {
      AppleTreeLocation: HasCarry & Any(
        Comment(
          "Grab the apple near the Winky Tree",
          Difficulty("Intermediate")
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
      LostleafLobbyDoor.define(_LostleafLobby.LostleafLakeDoor)
    ],

    region_connections = {
      OuterRim: Any(
        CanSuperJump,
        
        HasRoll & HasAirTail & Tech("ability_toggle") & HasDoubleJump,

        CanGroundTailJump & HasHighJump & HasDoubleJump & HasWings
      ),

      BellTower: Any(
        CanSuperJump,

        Comment(
          "Climb the ladder",
          Any(
            CanClimbPlantedTree,
            HasClimb & Any(
              CanTailJump(aerialExtraLogic = HasHighJump),
              HasDoubleJump,
              HasHorn,
              Comment(
                "Launch from the side of the church",
                HasRoll & HasAirTail
              )
            )
          )
        )
      ),

      RingBell: Any(
        Comment(
          "First-person snipe",
          HasBubble
        ),
        Comment(
          "Launch from the deep water and throw at a distance",
          HasSwim & Carrying("Bubble Conch")
        )
      )
    }
  ),
  
  BellTower.define(
    region_connections = {
      OuterRim: Any(
        HasWings,
        HasAirTail & HasRoll
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
