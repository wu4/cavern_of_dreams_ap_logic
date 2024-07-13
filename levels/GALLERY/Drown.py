from ...logic import lazy_region, Region, Entrance, Any, CarryableLocation
from ...logic import item, carrying

area_path = "DROWN/Drown (Main)"

class WaterLobbyDoor(Entrance):
  is_dest_underwater = True
  warp_path = f"{area_path}/Warps/WarpFromDrownToGallery"
  dest_path = f"{area_path}/Warps/DestIntoDrownPainting"

class BubbleConch(CarryableLocation): carryable = "Bubble Conch"

@lazy_region
def Main(r: Region):
  r.locations = {
    "Egg: Pits of Despair": item.horn
  }

  from . import WaterLobby

  r.entrances = [
    WaterLobbyDoor.define(WaterLobby.DrownPainting)
  ]

  r.region_connections = {
    BubbleConchPipe: Any(
      item.air_tail, item.ground_tail,
      carrying.bubble_conch, carrying.apple,
      item.horn
    ),
  }

@lazy_region
def BubbleConchPipe(r: Region):
  r.locations = {
    BubbleConch: item.carry
  }

  r.region_connections = {
    Main: None
  }
