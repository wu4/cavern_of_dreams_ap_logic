from ...logic import lazy_region, Region, Entrance

area_path = "UNDEAD/Undead (Main)"

class EarthLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromUndeadToGallery"
  dest_path = f"{area_path}/Warps/DestPaintingUndead"

@lazy_region
def Main(r: Region):
  r.locations = {
    "Egg: Wastes of Eternity": None
  }

  from . import EarthLobby

  r.entrances = [
    EarthLobbyDoor.define(EarthLobby.UndeadPainting)
  ]
