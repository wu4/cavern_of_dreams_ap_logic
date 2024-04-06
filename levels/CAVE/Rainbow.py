from ...logic import *

class Main(Region): pass
class MoonLedges(Region): pass
class ShroomLedges(Region): pass
class Topside(Region): pass

class Well(Entrance): pass

from ..CAVE.GalleryLobby import RainbowBench as _RainbowBench

regions = [
  Main.define(
    region_connections = {
      MoonLedges: Any(
        CanSuperJump,

        Comment(
          "Build height on the outside of the gate",
          Carrying("Jester Boots")
        ),

        Comment(
          "Conk on the geometry next to the ledge to short hop, then hijump",
          HasHighJump,
        ),

        HasHorn,

        Comment(
          "Jump from the well",
          Tech("tail_jump") & HasGroundTail & HasDoubleJump,
        ),
      )
    },

    entrances = [
      Well.define(_RainbowBench)
    ]
  ),

  MoonLedges.define(
    region_connections = {
      Main: None,

      ShroomLedges: Any(
        CanSuperJump,

        Carrying("Jester Boots"),

        HasBubble,
        
        HasDoubleJump,
        
        HasAirTail & HasRoll & Difficulty("Hard"),

        HasHorn & Tech("momentum_cancel")
      )
    }
  ),

  ShroomLedges.define(
    region_connections = {
      Main: None,

      Topside: Any(
        Comment(
          """Walk all of the way out of bounds to the green dragon, then
          carefully walk off to gain enough height for the final platform""",
          Difficulty("Hard") & Carrying("Jester Boots"),
        ),
        

        HasHorn,
        
        Comment(
          "Double jump after conking on the ceiling from the bouncy shroom",
          HasDoubleJump,
        ),
        
        HasHighJump & HasDoubleJump & Tech("momentum_cancel"),

        Comment(
          "Speedy roll, then jump into the bouncy shroom",
          HasAirTail & HasRoll,
        ),

        Tech("z_target") & HasBubble
      )
    }
  ),

  Topside.define(
    region_connections = {
      Main: None
    },

    locations = {
      "Card: Dream": Any(
        CanSuperJump,

        HasHighJump,

        HasDoubleJump,

        HasAirTail & HasRoll,
        
        HasHorn
      )
    }
  )
]