from logic import *
import LostleafLobby
import LostleafLake
import MoonCavern

class Main(Region): pass
class ArmadaLobbyRoom(Region): pass
class HighJumpLedge(Region): pass
class VineLedge(Region): pass
class TailSpinLedge(Region): pass
class MightyWallLedge(Region): pass
class WaterfallLedge(Region): pass
class DucklingsLedge(Region): pass
class DucklingsDoorway(Region): pass
class MoonCavernHeartDoorway(Region): pass

class LostleafLobbyDoor(Entrance): pass
class DucklingsDoorUpper(Entrance): pass
class DucklingsDoorLower(Entrance): pass
class MoonCavernHeartDoor(Entrance): pass

name = "Sun Cavern"

area = Area({
  Main: RegionDefinition(
    locations = {
      "Sun Cavern - Sage's Blessing 1": HasEggs(1),
      "Sun Cavern - Sage's Blessing 2": HasEggs(6),
      "Sun Cavern - Sage's Blessing 3": HasEggs(12),
      "Sun Cavern - Sage's Blessing 4": HasEggs(24),
      "Sun Cavern - Sage's Blessing 5": HasEggs(40),

      "Card: Sun Cavern - Air Vent": None,

      "Shroom: Sun Cavern - Mighty Wall Ground 1": None,
      "Shroom: Sun Cavern - Mighty Wall Ground 2": None,
      "Shroom: Sun Cavern - Mighty Wall Ground 3": None,
      "Shroom: Sun Cavern - Mighty Wall Ground 4": None
    },

    region_connections = {
      ArmadaLobbyRoom: Any(
        HasHorn,
        HasWings,

        Carrying("Jester Boots"),
        CanSuperJump,
        
        Comment(
          "Well-spaced high jump into the fan",
          HasHighJump & (HasSprint | CanBubbleJump)
        )
      ),

      HighJumpLedge: Any(
        HasHighJump,
        HasDoubleJump,

        Carrying("Jester Boots"),
        CanSuperJump,
        
        Comment(
          "Hover-jump into the nearby tutorial stone",
          CanHoverJump
        ),

        Comment(
          "Hover-shoot into the nearby tutorial stone",
          CanHoverShoot
        ),

        Comment(
          "Build speed and roll into the nearby tutorial stone",
          HasSprint & HasRoll
        )
      ),
      
      VineLedge: Any(
        HasClimb,
        CanSuperJump,
        
        Comment(
          "Hover-jump up the sun wall",
          CanHoverJump
        ),
        
        Comment(
          "Climb the nearby stalagmite or sun wall with hover + bubble shots",
          CanHoverShoot
        ),
        
        Comment(
          "Tail jump double jump from the nearby tutorial stone",
          HasDoubleJump & CanTailJump(
            groundedTail = HasHighJump | HasWings,
            aerialTail = HasHighJump & HasWings
          )
        )
      ),
      
      TailSpinLedge: Any(
        Carrying("Jester Boots"),
        CanSuperJump,

        Comment(
          "Roll jump makes the distance",
          HasRoll
        ),
        
        HasHighJump,
        
        HasBubble,

        HasWings,
        
        CanTailJump()
      ),

      MightyWallLedge: Any(
        HasClimb,
        Carrying("Jester Boots"),
        CanSuperJump,

        Comment(
          "Dive-bounce off of shroom",
          HasHorn
        ),

        Comment(
          "Jump up a tutorial stone and spire to reach the egg ledge",
          Any(
            HasDoubleJump & (HasHighJump | HasWings),

            All(
              Difficulty("Intermediate"),
              CanTailJump(
                groundedTail = None,
                aerialTail = HasHighJump | HasDoubleJump
              )
            )
          )
        ),
      ),

      WaterfallLedge: Any(
        Carrying("Jester Boots"),
        CanSuperJump,

        Comment(
          "Very high jump from one of the nearby gems",
          All (
            Difficulty("Intermediate"),
            Tech("tail_jump"),
            HasGroundTail & HasHighJump & HasDoubleJump & HasWings
          )
        )
      ),
      

      DucklingsLedge: Any(
        HasHorn,
        HasWings,
        HasDoubleJump,
        CanSuperJump,

        HasRoll & (HasSprint | HasAirTail),

        CanTailJump(
          groundedTail = None,
          aerialTail = Any(
            Comment(
              "Tail Spin from the right gem to the tiny leaf, then to the big leaf",
              Difficulty("Intermediate")
            ),
            HasHighJump
          )
        ),
      ),
      
      DucklingsDoorway: Any(
        CanSuperJump,

        Comment(
          "Speedy launch from the waterjet",
          HasSwim & (Difficulty("Intermediate") | HasSprint)
        ),
        
        Comment(
          "Float to the leaf from the Sage ramp",
          HasSprint & (CanHoverJump | CanBubbleJump)
        ),

        Comment(
          "Speedy launch from the Sage ramp",
          HasSprint & HasRoll & HasAirTail
        ),
        
        Comment(
          "Hover shoot from the Sage ramp",
          CanHoverShoot
        ),
        
        Comment(
          "Precise use of bubble float and shoot jumping to land on the leaf from the right gem",
          Difficulty("Intermediate") & CanBubbleJump
        ),
        
        Tech("momentum_cancel") & HasWings,

        Comment(
          "Clever use of wings and riding up the left gem's geometry to jump on a leaf",
          CanHoverJump
        )
      ),

      MoonCavernHeartDoorway:
        HasSwim & Any(
          HasHorn,
          Difficulty("Intermediate")
        )
    },
  ),

  ArmadaLobbyRoom: RegionDefinition(
    locations = {
      "Shroom: Sun Cavern - Armada Entrance 1" : None,
      "Shroom: Sun Cavern - Armada Entrance 2" : None,
      "Shroom: Sun Cavern - Armada Entrance 3" : None,
    },
    region_connections={
      Main: None
    }
  ),

  HighJumpLedge: RegionDefinition(
    locations = {
      "Shroom: Sun Cavern - High Jump Ledge 1": None,
      "Shroom: Sun Cavern - High Jump Ledge 2": None
    },
    region_connections = {
      Main: None
    }
  ),

  VineLedge: RegionDefinition(
    locations = {
      "Shroom: Sun Cavern - Vine Ledge 1": None,
      "Shroom: Sun Cavern - Vine Ledge 2": None
    },

    region_connections = {
      Main: None,
      HighJumpLedge: Any(
        CanHoverJump,
        HasRoll & (HasSprint | HasAirTail)
      )
    }
  ),

  TailSpinLedge: RegionDefinition(
    locations = {
      "Shroom: Sun Cavern - Tail Spin Ledge 1": None,
      "Shroom: Sun Cavern - Tail Spin Ledge 2": None
    },
      
    region_connections = {
      Main: None
    }
  ),

  MightyWallLedge: RegionDefinition(
    locations = {
      "Beat Mighty Wall": Any(
        HasAirTail,
        HasGroundTail,
        Carrying("Apple"),
        Carrying("Bubble Conch")
      ),

      "Egg: Sun Cavern - Mighty Wall": None,

      "Shroom: Sun Cavern - Mighty Wall Egg Ledge 1": None,
      "Shroom: Sun Cavern - Mighty Wall Egg Ledge 2": None,
      "Shroom: Sun Cavern - Mighty Wall Egg Ledge 3": None
    },

    entrances = {
      LostleafLobbyDoor: EntranceDefinition(
        to = LostleafLobby.SunCavernDoor,
        rule = HasEvent("Mighty Wall Toppled")
      )
    },

    region_connections = {
      Main: None
    }
  ),

  WaterfallLedge: RegionDefinition(
    locations = {
      "Egg: Sun Cavern - Waterfall": None
    },

    entrances = {
      DucklingsDoorUpper: EntranceDefinition(
        to = LostleafLake.DucklingsDoorUpper
      )
    },

    region_connections = {
      Main: None,
      
      DucklingsDoorway: Comment(
        "Simply float down",
        CanBubbleJump | CanHoverJump
      ),

      MoonCavernHeartDoorway: Comment(
        "Jumping down lets you get past the jets",
        HasSwim
      )
    }
  ),

  DucklingsLedge: RegionDefinition(
    locations = {
      "Shroom: Sun Cavern - Ducklings Ledge 1": None,
      "Shroom: Sun Cavern - Ducklings Ledge 2": None
    },

    region_connections = {
      Main: None,
      DucklingsDoorway: HighJumpObstacle | CanSuperJump
    }
  ),
  
  DucklingsDoorway: RegionDefinition(
    entrances = {
      DucklingsDoorLower: EntranceDefinition(
        to = LostleafLake.DucklingsDoorLower
      )
    },

    region_connections = {
      DucklingsLedge: None
    }
  ),

  MoonCavernHeartDoorway: RegionDefinition(
    entrances = {
      MoonCavernHeartDoor: EntranceDefinition(
        to = MoonCavern.SunCavernDoor,
        rule = HasEvent("Open Moon Cavern Heart Door")
      )
    },

    locations = {
      "Moon Cavern Heart Door": HasHearts(1) & CanWhack(ground_tail_works = True, air_tail_works = True)
    },

    region_connections = {
      Main: HasSwim
    }
  )
})

for region in area.regions:
  for k, v in region.locations.items():
    print(f"{k}: {v}")
  for k, v in region.region_connections.items():
    print(f"{region.__name__} -> {k.__name__}: {v}")