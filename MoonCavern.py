from logic import *

class Main(Region): pass
class DiveRoom(Region): pass
class DivePuzzleLedge(Region): pass
class UpperConnector(Region): pass
class Upper(Region): pass
class LavaMushroomPlatform(Region): pass
class DiveHoles(Region): pass
class NightmareLobbyDoorway(Region): pass

class SunCavernDoor(Entrance): pass
class PalaceLobbyDoor(Entrance): pass
class GalleryLobbyDoor(Entrance): pass

class DousedGalleryLobbyFlame(InternalEvent): pass

import SunCavern
import PalaceLobby
import GalleryLobby

area = Area({
  Main: RegionDefinition(
    locations = {
      "Card: Moon Cavern - Dive": HasSwim & CanWhack(horn_works = True),
      
      "Shroom: Moon Cavern - Lava Platforms 1": None,
      "Shroom: Moon Cavern - Lava Platforms 2": None,
      "Shroom: Moon Cavern - Lava Platforms 3": None,
      "Shroom: Moon Cavern - Lava Platforms 4": None,

      "Shroom: Moon Cavern - Potionfall": None,
    },

    entrances = {
      SunCavernDoor: EntranceDefinition(
        SunCavern.MoonCavernHeartDoor
      )
    },

    region_connections = {
      DiveHoles: CanWhack(horn_works = True),

      DiveRoom: Any(
        CanWhack(horn_works = True),

        Comment(
          "Vine entrance",
          CanWhack(air_tail_works = True, throwable_works = True)
        )
      ),

      DivePuzzleLedge: Any(
        HasHorn,

        CanSuperJump,
        Carrying("Jester Boots"),
        
        Comment(
          "Extinguish the Keehee and use him as a platform",
          Carrying("Potion") | HasBubble
        ),

        HasDoubleJump & CanTailJump(),

        HasWings & Any(
          HasDoubleJump,
          All(
            Tech("tail_jump") & HasGroundTail,
            Tech("hover_jump") | HasHighJump
          )
        )
      ),

      UpperConnector: Any(
        CanSuperJump,
        HighJumpObstacle,

        Comment(
          "Bouncy mushroom + Keehee damage boost",
          Tech("damage_boost")
        ),

        Comment(
          "Bouncy mushroom + Z-target bubble shooting",
          Tech("z_target") & CanBubbleJump
        ),

        Comment(
          "Hover from bouncy shroom",
          HasWings
        )
      ),

      Upper: Any(
        CanSuperJump,
        
        Comment(
          "Hover from bouncy shroom",
          HasWings
        ),

        Comment(
          "Bouncy mushroom + Keehee damage  boost while bubble floating",
          Tech("damage_boost") & CanBubbleJump
        )
      ),

      LavaMushroomPlatform: None
    }
  ),
  
  DiveHoles: RegionDefinition(
    locations = {
      "Shroom: Moon Cavern - Dive Holes 1": None,
      "Shroom: Moon Cavern - Dive Holes 2": None,
      "Shroom: Moon Cavern - Dive Holes 3": None,
      "Shroom: Moon Cavern - Dive Holes 4": None,
      "Shroom: Moon Cavern - Dive Holes 5": None,
      "Shroom: Moon Cavern - Dive Holes 6": None,
    },

    region_connections = {
      Main: None
    }
  ),

  UpperConnector: RegionDefinition(
    locations = {
      "Shroom: Moon Cavern - Lonely Shroom": None
    },

    region_connections = {
      Main: None,
      
      Upper: HighJumpObstacle
    }
  ),

  Upper: RegionDefinition(
    locations = {
      "Egg: Moon Cavern - Keehee Climb": Any(
        CanSuperJump,
        Carrying("Jester Boots"),

        DropCarryable(
          HasClimb & HasWings & (HasHighJump | HasHorn),
          throwable = True
        )
      ),

      "Card: Moon Cavern - Statue": None,

      "Shroom: Moon Cavern - Palace Lobby Entryway 1": None,
      "Shroom: Moon Cavern - Palace Lobby Entryway 2": None,
      "Shroom: Moon Cavern - Palace Lobby Entryway 3": None,
      "Shroom: Moon Cavern - Palace Lobby Pathway 1": None,
      "Shroom: Moon Cavern - Palace Lobby Pathway 2": None,
      "Shroom: Moon Cavern - Palace Lobby Pathway 3": None,
      "Shroom: Moon Cavern - Palace Lobby Statue 1": None,
      "Shroom: Moon Cavern - Palace Lobby Statue 2": None,
    },

    entrances = {
      PalaceLobbyDoor: EntranceDefinition(
        PalaceLobby.MoonCavernDoor
      )
    }
  ),

  LavaMushroomPlatform: RegionDefinition(
    locations = {
      "Shroom: Moon Cavern - Lava Mushroom Platform 1": None,
      "Shroom: Moon Cavern - Lava Mushroom Platform 2": None
    },

    region_connections = {
      Main: Any(
        HighJumpObstacle,

        Comment(
          "Boost off of the Keehee to the Dive Holes side",
          Tech("damage_boost") & Any(
            Difficulty("Hard"),
            CanBubbleJump
          )
        )
      ),

      NightmareLobbyDoorway: None
    }
  ),

  NightmareLobbyDoorway: RegionDefinition(
    locations = {
    },

    entrances = {
      GalleryLobbyDoor: EntranceDefinition(
        GalleryLobby.MoonCavernDoor,
        Any(
          HasInternalEvent(DousedGalleryLobbyFlame),
          DropCarryable(
            Difficulty("Hard") & Tech("momentum_cancel"),
            jester_boots = True,
            throwable = True
          )
        )
      )
    }
  )
})