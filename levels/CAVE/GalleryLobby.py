from ...logic.objects import Region, Entrance
from ...logic.comment import Comment
from ...logic import All, Any
from ...logic import event, tech, item, carrying, difficulty

class Main(Region): pass
class LostleafCave(Region): pass
class OuterWalls(Region): pass
class Maze(Region): pass

class LostleafLobbyDoor(Entrance): pass
class MoonCavernDoor(Entrance): pass
class SunCavernTeleport(Entrance): pass
class RainbowBench(Entrance): pass
class FoyerDoor(Entrance): pass

from . import LostleafLobby as _LostleafLobby
from . import SunCavern as _SunCavern
from . import MoonCavern as _MoonCavern
from . import Rainbow as _Rainbow
from ..GALLERY import Foyer as _Foyer

[UNFINISHED]

regions = [
  Main.define(
    locations = {
      "Card: Gallery Lobby - Behind the Gallery": None,

      "Shroom: Gallery Lobby - Fountain 1": None,
      "Shroom: Gallery Lobby - Fountain 2": None,
      "Shroom: Gallery Lobby - Fountain 3": None,
      "Shroom: Gallery Lobby - Fountain 4": None,

      "Shroom: Gallery Lobby - Castle Hill 1": None,
      "Shroom: Gallery Lobby - Castle Hill 2": None,
      "Shroom: Gallery Lobby - Castle Hill 3": None,
      "Shroom: Gallery Lobby - Castle Hill 4": None,
      "Shroom: Gallery Lobby - Castle Hill 5": None,

      "Shroom: Gallery Lobby - Entryway 1": None,
      "Shroom: Gallery Lobby - Entryway 2": None,
      "Shroom: Gallery Lobby - Entryway 3": None,
      "Shroom: Gallery Lobby - Entryway 4": None,
      "Shroom: Gallery Lobby - Entryway 5": None,
    },
    
    entrances = [
      FoyerDoor.define(
        to = _Foyer.GalleryLobbyDoor,
        rule = event.Collected("Open Gallery Lobby Door")
      ),
      RainbowBench.define(
        to = _Rainbow.Well
      )
    ],

    region_connections = {
      OuterWalls: Any(
        tech.AnySuperJump,
        carrying.JesterBoots,

        difficulty.Intermediate & item.Roll & item.Sprint
      ),

      LostleafCave: Any(
        tech.AnySuperJump,
        carrying.JesterBoots
      ),

      Maze: Any(
        tech.AnySuperJump,
        event.Collected("Open Gallery Lobby Hedge Maze"),
        carrying.JesterBoots,
        
        tech.GroundTailJump & item.HighJump & item.DoubleJump,
        
        Comment(
          "Jump from the hedges",
          item.Wings & item.DoubleJump,
        ),

        Comment(
          "Fastroll jump from the fountain walls, then hover over the gate",
          item.Roll & item.AirTail & item.Wings
        )
      )

    }
  ),

  LostleafCave.define(
    locations = {
      "Egg: Gallery Lobby - Lostleaf Lobby Entryway": None
    },

    entrances = [
      LostleafLobbyDoor.define(_LostleafLobby.GalleryLobbyDoor)
    ],

    region_connections = {
      Main: Any(
        tech.AnySuperJump,
        carrying.JesterBoots,
        item.DoubleJump & carrying.PlantAndClimbTree
      )
    }
  ),

  OuterWalls.define(
    region_connections = {
      Main: None,
      Maze: Any(
        item.Wings,
        item.Bubble & tech.MomentumCancel
      ),
      LostleafCave: Any(
        item.Wings,
        item.Bubble,
        tech.MomentumCancel
      )
    }
  ),

  Maze.define(
    locations = {
      "Card: Gallery Lobby - Hedge Maze": None,

      "Gallery Lobby - Hedge Maze Preston": Any(
        tech.AnySuperJump,
        carrying.JesterBoots,
        
        event.Collected("Open Gallery Lobby Door"), # ???
        
        item.Bubble & Any(
          item.DoubleJump,
          item.Horn,
          tech.GroundTailJump,
          tech.AirTailJump & item.HighJump
        ),

        item.DoubleJump & Any(
          item.Horn,
          tech.GroundTailJump,
          item.HighJump & item.Wings,
          tech.AirTailJump & (item.Wings | item.HighJump)
        )
      )
    },
    region_connections = {
      Main: Any(
        tech.AnySuperJump,
        carrying.JesterBoots,

        event.Collected("Open Gallery Lobby Hedge Maze")
      )
    }
  )
]