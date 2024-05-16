from ...logic.objects import Region, Entrance
from ...logic.comment import Comment
from ...logic import Any
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

from . import LostleafLobby
from . import SunCavern
from . import MoonCavern
from . import Rainbow
from ..GALLERY import Foyer

# [UNFINISHED]

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
        to = Foyer.GalleryLobbyDoor,
        rule = event.Collected("Open Gallery Lobby Door")
      ),
      RainbowBench.define(
        to = Rainbow.Well
      )
    ],

    region_connections = {
      OuterWalls: Any(
        tech.any_super_jump,
        carrying.jester_boots,

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
      )

    }
  ),

  LostleafCave.define(
    locations = {
      "Egg: Gallery Lobby - Lostleaf Lobby Entryway": None
    },

    entrances = [
      LostleafLobbyDoor.define(LostleafLobby.GalleryLobbyDoor)
    ],

    region_connections = {
      Main: Any(
        tech.any_super_jump,
        carrying.jester_boots,
        item.double_jump & carrying.plant_and_climb_tree
      )
    }
  ),

  OuterWalls.define(
    region_connections = {
      Main: None,
      Maze: Any(
        item.wings,
        item.bubble & tech.momentum_cancel
      ),
      LostleafCave: Any(
        item.wings,
        item.bubble,
        tech.momentum_cancel
      )
    }
  ),

  Maze.define(
    locations = {
      "Card: Gallery Lobby - Hedge Maze": None,

      "Gallery Lobby - Hedge Maze Preston": Any(
        tech.any_super_jump,
        carrying.jester_boots,

        event.Collected("Open Gallery Lobby Door"), # ???

        item.bubble & Any(
          item.double_jump,
          item.horn,
          tech.ground_tail_jump,
          tech.air_tail_jump & item.high_jump
        ),

        item.double_jump & Any(
          item.horn,
          tech.ground_tail_jump,
          item.high_jump & item.wings,
          tech.air_tail_jump & (item.wings | item.high_jump)
        )
      )
    },
    region_connections = {
      Main: Any(
        tech.any_super_jump,
        carrying.jester_boots,

        event.Collected("Open Gallery Lobby Hedge Maze")
      )
    }
  )
]
