from typing import override
from ...logic.objects import EntranceType, InternalEvent, PlantableSoil
from ...logic import Region, Entrance, Any
from ...logic.objects import CarryableLocation
from ...logic.comment import Comment
from ...logic import item, difficulty, tech, carrying, event, has, templates

class PrestonAccess(InternalEvent): pass

class Main(Region):
  pass

class LeftPlatform(Region):
  pass

class RightPlatform(Region):
  pass

class EggPlatform(Region):
  locations = {
    "Egg: Crypt - Shelwart's Gravestone": Any(
      (item.bubble | difficulty.intermediate) & Any(
        item.double_jump,
        item.high_jump,
      ),
      tech.ground_tail_jump,

      item.high_jump & Any(
        item.double_jump,
      ),

      item.horn,
    )
  }

class BackExit(Region):
  pass

class PrestonRoom(Region):
  locations = {
    PrestonAccess: None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None
    }
