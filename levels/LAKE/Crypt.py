from ...logic.objects import EntranceType, InternalEvent, PlantableSoil
from ...logic import lazy_region, Region, Entrance, Any
from ...logic.objects import CarryableLocation
from ...logic.comment import Comment
from ...logic import item, difficulty, tech, carrying, event, has, templates

class PrestonAccess(InternalEvent): pass

@lazy_region
def Main(r: Region):
  pass

@lazy_region
def LeftPlatform(r: Region):
  pass

@lazy_region
def RightPlatform(r: Region):
  pass

@lazy_region
def EggPlatform(r: Region):
  r.locations = {
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

@lazy_region
def BackExit(r: Region):
  pass

@lazy_region
def PrestonRoom(r: Region):
  r.locations = {
    PrestonAccess: None
  }

  r.region_connections = {
    Main: None
  }
