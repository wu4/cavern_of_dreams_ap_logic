from logic import *

class Main(Region): pass
class Trees(Region): pass
class HiddenWall(Region): pass
class HiddenDoorway(Region): pass

class SunCavernDoor(Entrance): pass
class LostleafLakeDoor(Entrance): pass

import SunCavern
import LostleafLake

CanOpenHiddenWall: Logic = CanWhack(ground_tail_works = True, air_tail_works = True, roll_works = True, throwable_works = True)

area = Area({
  Main: RegionDefinition(
    locations = {
      "Shroom: Lostleaf Lobby - Bridge 1": None,
      "Shroom: Lostleaf Lobby - Bridge 2": None,
      "Shroom: Lostleaf Lobby - Bridge 3": None
    },

    entrances = {
      SunCavernDoor: EntranceDefinition(
        SunCavern.LostleafLobbyDoor
      ),

      LostleafLakeDoor: EntranceDefinition(
        LostleafLake.LostleafLobbyDoor
      )
    },

    region_connections = {
      HiddenWall: CanOpenHiddenWall,

      Trees: Any(
        Difficulty("Intermediate"),
        HighJumpObstacle
      )
    },
    
  )
})