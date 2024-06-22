from logic import has
from ...logic.objects import Region, Entrance
from ...logic.comment import Comment
from ...logic import Any
from ...logic import event, tech, item, carrying, difficulty
from ...logic.objects import PlantableSoil

class Main(Region): pass
class LostleafCave(Region): pass
class OuterWalls(Region): pass
class Maze(Region): pass
class MazeStatue(Region): pass

class LostleafLobbyDoor(Entrance): pass
class MoonCavernDoor(Entrance): pass
class SunCavernTeleport(Entrance): pass
class RainbowBench(Entrance): pass
class FoyerDoor(Entrance): pass

class GalleryLobbySoil(PlantableSoil): pass


from . import LostleafLobby
from . import SunCavern
from . import MoonCavern
from . import Rainbow
from ..GALLERY import Foyer

regions = [
  Main.define(
    locations = {
      "Card: Gallery Lobby - Behind the Gallery": None,

      "Gallery Lobby - Extinguish Torches": item.bubble,

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
        default_connection = Foyer.GalleryLobbyDoor,
        rule = event.Collected("Open Gallery Lobby Door")
      ),
      MoonCavernDoor.define(
        default_connection = MoonCavern.GalleryLobbyDoor
      ),
      SunCavernTeleport.define(
        default_connection = SunCavern.GalleryLobbyTeleport,
        rule = event.Collected("Open Gallery Lobby Teleport")
      ),
      RainbowBench.define(
        default_connection = Rainbow.Well
      )
    ],

    region_connections = {
      OuterWalls: Any(
        tech.any_super_jump,
        carrying.jester_boots,

        Comment(
          "The hole in the wall to the right of the Foyer entrance lets you slide up",
          carrying.mr_kerringtons_wings,
        ),

        Comment(
          "Tailjump double jump onto the Foyer entrance, then tailspin roll jump over to the walls",
          item.double_jump & tech.ground_tail_jump & item.roll & item.air_tail,
        ),

        difficulty.intermediate & item.roll & item.sprint
      ),

      LostleafCave: Any(
        tech.any_super_jump,
        carrying.jester_boots
      ),

      Maze: Any(
        tech.any_super_jump,
        event.Collected("Open Gallery Lobby Hedge Maze"),
        carrying.jester_boots,

        tech.ground_tail_jump & item.high_jump & item.double_jump,

        Comment(
          "Jump from the hedges",
          item.wings & item.double_jump,
        ),

        Comment(
          "Fastroll jump from the fountain walls, then hover over the gate",
          item.roll & item.air_tail & item.wings
        )
      ),

      MazeStatue: Any(
        Comment(
          "Carry height into the maze and jump over the rose bush",
          carrying.jester_boots
        )
      )
    }
  ),

  LostleafCave.define(
    locations = {
      "Egg: Gallery Lobby - Lostleaf Lobby Entryway": None,
      GalleryLobbySoil: carrying.apple
    },

    entrances = [
      LostleafLobbyDoor.define(LostleafLobby.GalleryLobbyDoor)
    ],

    region_connections = {
      Main: Any(
        tech.any_super_jump,
        carrying.jester_boots,
        event.Collected(GalleryLobbySoil) & item.climb & item.double_jump
      )
    }
  ),

  OuterWalls.define(
    region_connections = {
      Main: None,

      Maze: Any(
        item.wings,
        carrying.mr_kerringtons_wings,
        tech.bubble_jump & (tech.momentum_cancel | item.double_jump)
      ),

      LostleafCave: Any(
        item.wings,
        carrying.mr_kerringtons_wings,
        item.double_jump,
        tech.bubble_jump,
        tech.momentum_cancel
      )
    }
  ),

  Maze.define(
    locations = {
      "Card: Gallery Lobby - Hedge Maze": None
    },

    region_connections = {
      Main: Any(
        tech.any_super_jump,
        carrying.jester_boots,

        event.Collected("Open Gallery Lobby Hedge Maze")
      ),

      MazeStatue: Any(
        tech.any_super_jump,

        carrying.jester_boots & Any(
          Comment(
            "Walk outside of the maze near its entrance and repeatedly walk into an invisible wall to gain height",
            tech.out_of_bounds
          ),

          item.double_jump,
          tech.ground_tail_jump
        ),

        event.Collected("Open Gallery Lobby Door"),

        Comment("Water the rose", item.bubble) & Any(
          Comment(
            "Jump onto the rose as it grows",
            tech.ejection_launch
          ),

          item.double_jump,
          item.horn,
          tech.ground_tail_jump,
          tech.air_tail_jump & item.high_jump,
        ),

        item.double_jump & Any(
          item.horn,
          tech.ground_tail_jump,
          item.high_jump & item.wings,
          difficulty.intermediate & tech.air_tail_jump & item.high_jump
        )
      )
    }
  ),

  MazeStatue.define(
    locations = {
      "Gallery Lobby - Hedge Maze Preston": None
    },

    region_connections = {
      Maze: Any(
        event.Collected("Open Gallery Lobby Door"),

        tech.any_super_jump,

        tech.ground_tail_jump & item.double_jump & item.wings & item.high_jump
      )
    }
  )
]
