from logic import *

class Main(Region): pass
class Trees(Region): pass
class HiddenDoorway(Region): pass

class SunCavernDoor(Entrance): pass
class LostleafLakeDoor(Entrance): pass
class GalleryLobbyDoor(Entrance): pass

import SunCavern
import LostleafLake
import GalleryLobby

CanBreakHiddenWall: Logic = CanWhack(ground_tail_works = True, air_tail_works = True, roll_works = True, throwable_works = True)

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
      HiddenDoorway: CanBreakHiddenWall,

      Trees: Difficulty("Intermediate") | HighJumpObstacle
    },
  ),

  Trees: RegionDefinition(
    locations = {
      "Shroom: Lostleaf Lobby - Trees 1": None,
      "Shroom: Lostleaf Lobby - Trees 2": None,
      "Shroom: Lostleaf Lobby - Trees 3": None,
      
      "Egg: Lostleaf Lobby - Branches": None,
      
      "Card: Lostleaf Lobby - Branches": None,
    },

    region_connections = {
      Main: None
    }
  ),
  
  HiddenDoorway: RegionDefinition(
    entrances = {
      GalleryLobbyDoor: EntranceDefinition(
        GalleryLobby.LostleafLobbyDoor
      )
    },

    region_connections = {
      Main: CanBreakHiddenWall
    }
  )
})