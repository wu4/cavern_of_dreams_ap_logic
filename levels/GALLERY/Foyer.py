from ...logic import lazy_region, Region, Entrance, Any, InternalEvent
from ...logic import item, carrying, tech, event, difficulty
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

class OpenedGratitudeDoor(InternalEvent): pass

@lazy_region
def Main(r: Region):
  r.locations = {
    OpenedGratitudeDoor: HasGratitude(4) & (item.air_tail | item.ground_tail),
    "Foyer - Sage's Painting": carrying.sages_gloves,
    "Card: Foyer - Water Lobby Entrance": Any(
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
    "Egg: Foyer - Matryoshka Egg": Any(
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
    SideDoors: event.Collected("Open Foyer Doors"),
    Finale: event.Collected(OpenedGratitudeDoor)
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
def Finale(r: Region):
  r.region_connections = {
    Endgame: Any(
      item.swim & item.wings,

      (item.sprint | difficulty.intermediate) & Any(
        carrying.mr_kerringtons_wings,
        item.wings & item.double_jump,
      ),

      difficulty.intermediate & Any(
        item.wings & item.double_jump & tech.ability_toggle,
        item.swim & Any(carrying.bubble_conch, carrying.shelnerts_fish),
      ),

      difficulty.hard & Any(
        item.swim & Any(
          tech.momentum_cancel & tech.damage_boost,
          tech.bubble_jump,
        ),
      )
    )
  }

@lazy_region
def Endgame(r: Region):
  pass
