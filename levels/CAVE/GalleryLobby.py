from ...logic import *

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
        rule = Has("Open Gallery Lobby Door")
      ),
      RainbowBench.define(
        to = _Rainbow.Well
      )
    ],

    region_connections = {
      OuterWalls: Any(
        CanSuperJump,
        Carrying("Jester Boots"),

        Difficulty("Intermediate") & HasRoll & HasSprint
      ),

      LostleafCave: Any(
        CanSuperJump,
        Carrying("Jester Boots")
      ),

      Maze: Any(
        CanSuperJump,
        Has("Open Gallery Lobby Hedge Maze"),
        Carrying("Jester Boots"),
        
        HasGroundTail & Tech("tail_jump") & HasHighJump & HasDoubleJump,
        
        Comment(
          "Jump from the hedges",
          HasWings & HasDoubleJump,
        ),

        Comment(
              #Fastroll jump from the fountain walls, then hover over the gate
          "",
          HasRoll & HasAirTail & HasWings
        )
      )

          # - comment: >
          #     Launch onto the walls using the steep hill, then float over the
          #     gate
          #   and:
          #   - movement: 3
          #   - ability: Roll
          #   - ability: Sprint
          #   - or:
          #     - ability: Hover
          #     - and:
          #       - ability: Bubble
          #       - tech: momentum_cancel
    }
  )
]

  Start:
    area_connections:
      Lostleaf Lobby Connector:
        or:
          - tech: super_bounce
          - tech: bubble_jump

      Maze:
        or:
          - event: Open Gallery Lobby Hedge Maze
          - tech: bubble_jump
          - tech: super_bounce
          - carrying: Jester Boots

          - and:
            - ability: Grounded Attack
            - ability: High Jump
            - ability: Double Jump
          - and:
            - ability: Hover
            - ability: Double Jump
          - comment: >
              Launch onto the walls using the steep hill, then float over the
              gate
            and:
            - movement: 3
            - ability: Roll
            - ability: Sprint
            - or:
              - ability: Hover
              - and:
                - ability: Bubble
                - tech: momentum_cancel
          - comment: >
              Fastroll jump from the fountain walls, then hover over the gate
            and:
            - movement: 3
            - ability: Roll
            - ability: Aerial Attack
            - ability: Hover

  Lostleaf Lobby Connector:
    area_connections:
      Start:
        or:
          - tech: super_bounce
          - tech: bubble_jump
          - carrying: Jester Boots
    
    locations:
      eggs:
        Lostleaf Lobby Entryway:
          null
        
    entrances:
      Lostleaf Lobby Door:
        to:
          - Lostleaf Lobby
          - Gallery Lobby Door

  Outer Walls:
    area_connections:
      Maze:
        or:
          - ability: Hover
          - and:
            - tech: momentum_cancel
            - ability: Bubble

      Lostleaf Lobby Connector:
        or:
          - ability: Hover
          - ability: Bubble
    
  Maze:
    area_connections:
      Start:
        or:
          - event: Open Gallery Lobby Hedge Maze
          - tech: bubble_jump
          - tech: super_bounce
          - carrying: Jester Boots

    locations:
      events:
        Hedge Maze Preston:
          or:
            - tech: super_bounce

            - carrying: Jester Boots

            - event: Open Gallery Lobby Door
            - and:
              - ability: Bubble
              - or:
                - ability: Double Jump
                - ability: Dive
                - ability: Grounded Attack
                - and:
                  - ability: Aerial Attack
                  - ability: High Jump
            - and:
              - ability: Double Jump
              - or:
                - ability: Dive
                - ability: Grounded Attack
                - and:
                  - ability: High Jump
                  - ability: Hover
                - and:
                  - ability: Aerial Attack
                  - or:
                    - ability: High Jump
                    - ability: Hover
      cards:
        Hedge Maze:
          null