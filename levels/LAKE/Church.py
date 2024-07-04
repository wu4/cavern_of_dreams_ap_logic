from typing import override
from ...logic.objects import EntranceType
from ...logic import Region, Entrance, Any
from ...logic import item, tech, carrying, event

class LostleafLakeDoor(Entrance): pass

class Main(Region):
  locations = {
    "Shroom: Church - Pews 1": None,
    "Shroom: Church - Pews 2": None,
    "Shroom: Church - Pews 3": None,
    "Shroom: Church - Pews 4": None,

    "Church - Angel Statue Puzzle": Any(
      item.air_tail | item.ground_tail,
      carrying.apple | carrying.bubble_conch
    ),

    "Card: Church - Top": Any(
      item.wings & Any(
        item.double_jump,
        tech.bubble_jump_and_recoil
      ),
      item.sprint,
      carrying.bubble_conch
    )
  }
  @override
  @classmethod
  def load(cls):
    from . import LostleafLake
    cls.entrances = [
      LostleafLakeDoor.define(
        default_connection = LostleafLake.ChurchDoor,
        type = EntranceType.BILINEAR | EntranceType.UNDERWATER
      )
    ]

    cls.region_connections = {
      Basement: event.Collected("Open Church Basement")
    }

class Basement(Region):
  locations = {
    "Egg: Church - Below the Angel Statues": None
  }

  @override
  @classmethod
  def load(cls):
    cls.region_connections = {
      Main: None
    }
