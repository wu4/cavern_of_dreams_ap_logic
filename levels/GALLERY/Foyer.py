from ...logic import lazy_region, Region, Entrance, Any
from ...logic import item, carrying, tech, event
from ...logic.quantities import HasGratitude

area_path = "GALLERY/Foyer (Main)"

class GalleryLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromFoyerToGalleryLobby"
  dest_path = f"{area_path}/Warps/DestFromGalleryLobbyToFoyer"
class WaterLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromFoyerToWaterLobby"
  dest_path = f"{area_path}/Warps/DestFromWaterLobbyToFoyer"
class EarthLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromFoyerToEarthLobby"
  dest_path = f"{area_path}/Warps/DestFromEarthLobbyToFoyer"
class FireLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromFoyerToFireLobby"
  dest_path = f"{area_path}/Warps/DestFromFireLobbyToFoyer"
# class AtelierDoor(Entrance):
#   warp_path = f"{area_path}/Warps/WarpFromFoyerToAtelier"
#   dest_path = f"{area_path}/Warps/DestFromAtelierToFoyer"
class WaterLobbyHole(Entrance):
  warp_path = f"{area_path}/Warps/WarpTrapdoor"

@lazy_region
def Main(r: Region):
  r.locations = {
    "Gallery of Nightmares - Sage's Painting": carrying.sages_gloves,
    "Card: Gallery of Nightmares - Basement Entrance": Any(
      item.wings,
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
      item.double_jump,
      tech.bubble_jump & Any(
        item.roll,
        item.horn,
        item.high_jump,
        item.sprint
      ),
      tech.ground_tail_jump,
      tech.air_tail_jump,
    ),
    "Egg: Gallery of Nightmares - Matryoshka Egg": Any(
      item.horn,
      tech.ground_tail_jump,
      item.air_tail,
      carrying.apple | carrying.bubble_conch
    )
  }

  from ..CAVE import GalleryLobby
  from . import WaterLobby

  r.entrances = [
    GalleryLobbyDoor.define(GalleryLobby.FoyerDoor),
    WaterLobbyDoor.define(WaterLobby.FoyerDoor),
    WaterLobbyHole.define(WaterLobby.FoyerHole)
  ]

  r.region_connections = {
    SideDoors: event.Collected("Open Gallery Doors"),
    Endgame: HasGratitude(4) & (item.air_tail | item.ground_tail) & item.swim
  }

@lazy_region
def SideDoors(r: Region):
  r.region_connections = {
    Main: None
  }

  from . import FireLobby
  from . import EarthLobby

  r.entrances = [
    FireLobbyDoor.define(FireLobby.FoyerDoor),
    EarthLobbyDoor.define(EarthLobby.FoyerDoor)
  ]

@lazy_region
def Endgame(r: Region):
  pass