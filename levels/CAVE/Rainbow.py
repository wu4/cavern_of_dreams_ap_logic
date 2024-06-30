from typing import override

from ...logic.comment import Comment
from ...logic import Any, Region, Entrance
from ...logic import item, tech, carrying, difficulty

class WellEntrance(Entrance): pass

class Main(Region):
  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      MoonLedges: Any(
        tech.any_super_jump,

        Comment(
          "Build height on the outside of the gate",
          carrying.jester_boots
        ),

        Comment(
          "Conk on the geometry next to the ledge to short hop, then hijump",
          item.high_jump
        ),

        item.horn,

        Comment(
          "Jump from the well",
          tech.ground_tail_jump & item.double_jump,
        ),
      ),

      Well: Any(
        carrying.jester_boots,
        carrying.mr_kerringtons_wings,
        tech.bubble_jump,
        item.double_jump,
        tech.air_tail_jump,
        tech.ground_tail_jump,
        item.sprint & item.roll,
        tech.momentum_cancel & item.high_jump
      )
    }

class MoonLedges(Region):
  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None,

      Well: None,

      ShroomLedges: Any(
        tech.any_super_jump,

        carrying.jester_boots,

        carrying.mr_kerringtons_wings & Any(
          # this is technically performable without any bonus items
          # but it becomes a lot more consistent with them
          # losing a temporary item after 1 failed attempt would kinda suck
          item.sprint,
          tech.momentum_cancel & item.high_jump,
          item.double_jump
        ),

        item.bubble,

        item.double_jump,

        item.air_tail & item.roll & difficulty.hard,

        item.horn & Any(
          item.wings,
          tech.momentum_cancel
        )
      )
    }

class ShroomLedges(Region):
  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None,

      Topside: Any(
        Comment(
          """Walk all of the way out of bounds to the green dragon, then
          carefully walk off to gain enough height for the final platform""",
          difficulty.hard & carrying.jester_boots
        ),


        item.horn,

        Comment(
          "Double jump after conking on the ceiling from the bouncy shroom",
          item.double_jump
        ),

        item.high_jump & item.double_jump & tech.momentum_cancel,

        Comment(
          "Speedy roll, then jump into the bouncy shroom",
          item.air_tail & item.roll,
        ),

        tech.z_target & tech.bubble_jump
      )
    }

class Topside(Region):
  locations = {
    "Card: Dream": Any(
      tech.any_super_jump,

      item.high_jump,

      item.double_jump,

      item.air_tail & item.roll,

      item.horn
    )
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None
    }

class Well(Region):
  @override
  @classmethod
  def load(cls):
    from . import GalleryLobby

    cls.region_connections = {
      Main: None
    }

    cls.entrances = [
      WellEntrance.define(
        default_connection = GalleryLobby.RainbowBench,
      )
    ]
