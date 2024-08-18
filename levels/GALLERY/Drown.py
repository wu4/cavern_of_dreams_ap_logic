from ...logic.objects import Whackable
from ...logic import lazy_region, Region, Entrance
from ...logic import item, carrying

area_path = "DROWN/Drown (Main)"

class WaterLobbyDoor(Entrance):
  is_dest_underwater = True
  warp_path = f"{area_path}/Warps/WarpFromDrownToGallery"
  dest_path = f"{area_path}/Warps/DestIntoDrownPainting"

class BubbleConchWhackableWall(Whackable):
  air_tail_works = True
  ground_tail_works = True
  throwables_work = True
  horn_works = True

@lazy_region
def Entry(r: Region):
  from . import WaterLobby

  r.entrances = [
    WaterLobbyDoor.define(
      WaterLobby.DrownPainting,
      carrying.no_jester_boots
    )
  ]

  r.region_connections = {
    Main: carrying.no_jester_boots
  }

@lazy_region
def Main(r: Region):
  r.locations = {
    "Egg: Pits of Despair": item.horn
  }

  r.region_connections = {
    Entry: None,
    **BubbleConchWhackableWall.connecting_to(BubbleConchPipe)
  }

@lazy_region
def BubbleConchPipe(r: Region):
  r.locations = {
    "Pits of Despair - Bubble Conch": None
  }

  r.region_connections = {
    **BubbleConchWhackableWall.connecting_to(Main)
  }
