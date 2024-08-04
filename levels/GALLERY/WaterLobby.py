from ...logic import Whackable, lazy_region, Region, Entrance, InternalEvent, Any
from ...logic import item, carrying, tech, templates, event
from ...logic.comment import Comment

area_path = "GALLERY/Water Lobby"

class LunaRoomDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromWaterLobbyToSecretRoom"
  dest_path = f"{area_path}/Warps/DestFromSecretRoomToWaterLobby"

class SewerDoor(Entrance):
  is_dest_underwater = True
  warp_path = f"{area_path}/Warps/WarpFromWaterLobbyToSewer"
  dest_path = f"{area_path}/Warps/DestFromSewerToWaterLobby"

class FoyerDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromWaterLobbyToFoyer"
  dest_path = f"{area_path}/Warps/DestFromFoyerToWaterLobby"

class FoyerHole(Entrance):
  dest_path = f"{area_path}/Warps/DestTrapdoor"

class CenterDrain(Entrance):
  dest_path = f"{area_path}/Warps/DestPitCenter HEXAGON"

class FarDrain(Entrance):
  dest_path = f"{area_path}/Warps/DestPitMoon CROSS"

class GiantDrain(Entrance):
  dest_path = f"{area_path}/Warps/DestPitLake DELTA"

class EggDrain(Entrance):
  dest_path = f"{area_path}/Warps/DestPitNearPainting DIAMOND"

class DrownPainting(Entrance):
  _painting_path = f"{area_path}/Objects Center/PaintingWarpDROWN"
  warp_path = f"{_painting_path}/WarpCutscene/WarpEvent"
  dest_path = f"{_painting_path}/DestFromPaintingDROWN"

class AirSwimFromMain(InternalEvent): pass
class AirSwimFromSpooky(InternalEvent): pass

class SpookyWall(Whackable):
  ground_tail_works = True
  air_tail_works = True
  bubble_works = True
  throwables_work = True

@lazy_region
def Main(r: Region):
  r.locations = {
    "Card: Water Lobby - Above Pits of Despair Painting": Any(
      event.Collected(AirSwimFromMain),
      carrying.jester_boots & Any(
        tech.super_bubble_jump,
        tech.ground_tail_jump,
        item.air_tail,
        item.high_jump,
        item.horn,
        item.double_jump,
      )
    ),
    "Water Lobby - Sage's Gloves": templates.high_jump_obstacle,
    AirSwimFromMain: item.swim & item.air_swim,
  }

  from . import Foyer, Drown

  r.entrances = [
    FoyerDoor.define(Foyer.WaterLobbyDoor),
    FoyerHole.define(Foyer.WaterLobbyHole),
    DrownPainting.define(
      default_connection = Drown.WaterLobbyDoor,
      rule = Any(
        event.Collected(AirSwimFromMain),
        carrying.jester_boots,
        tech.wing_jump & Any(
          tech.bubble_jump_and_recoil & tech.z_target & tech.ground_tail_jump & item.double_jump
        ),
        carrying.mr_kerringtons_wings & Any(
          item.sprint & item.double_jump,

          tech.bubble_jump_and_recoil & tech.z_target &
            (item.high_jump | item.double_jump),

          item.high_jump & Any(
            tech.ability_toggle & item.double_jump,
            item.sprint,
          )
        )
      )
    )
  ]

  r.region_connections = {
    LobbySewerMiddle: None,
    **SpookyWall.connecting_to(Spooky)
  }

@lazy_region
def LunaHouse(r: Region):
  from . import LunaRoom

  r.entrances = [
    LunaRoomDoor.define(LunaRoom.WaterLobbyDoor)
  ]

  r.region_connections = {
    Spooky: event.Collected("Open Luna's House")
  }

class ReachSpookyPlatform(InternalEvent): pass

@lazy_region
def Spooky(r: Region):
  r.locations = {
    ReachSpookyPlatform: Any(
      event.Collected(AirSwimFromSpooky),
      event.Collected(AirSwimFromMain),
      carrying.jester_boots,
      templates.high_jump_obstacle
    ),
    "Water Lobby - Angel Statue Puzzle": event.Collected(ReachSpookyPlatform) & Any(
      item.air_tail, item.ground_tail,
      carrying.bubble_conch, carrying.apple,
    ),
    AirSwimFromSpooky: item.swim & item.air_swim,
    "Water Lobby - Lady Opal's Head": event.Collected("Open Water Lobby Chest #1")
  }

  r.region_connections = {
    LunaHouse: event.Collected("Open Luna's House"),
    SpookyWaterUpper: item.swim,
    **SpookyWall.connecting_to(Main)
  }

@lazy_region
def SpookyWaterUpper(r: Region):
  r.locations = {
    "Water Lobby - Lady Opal's Painting": carrying.lady_opals_head,
    "Water Lobby - Jester Boots": event.Collected("Open Water Lobby Chest #2"),
  }

  r.region_connections = {
    Spooky: None,
    SpookyWaterLower: item.horn
  }

@lazy_region
def SpookyWaterLower(r: Region):
  r.locations = {
    "Egg: Water Lobby - Deepest Darkness": None
  }

  r.region_connections = {
    SpookyWaterUpper: None
  }

@lazy_region
def LobbySewerMiddle(r: Region):
  from . import EarthLobby

  r.entrances = [
    CenterDrain.define(EarthLobby.ToiletBridge),
    FarDrain.define(EarthLobby.ToiletDragonHead)
  ]

  r.region_connections = {
    Main: Any(
      carrying.jester_boots,
      tech.any_super_jump,
      item.horn,
      item.double_jump,
      tech.ground_tail_jump,
      tech.air_tail_jump & item.high_jump
    ),

    LobbySewerEgg: Any(
      tech.any_super_jump,
      Comment(
        "Use the paintings as platforms",

        Any(
          carrying.jester_boots,

          item.double_jump & Any(
            tech.ground_tail_jump & tech.bubble_jump,
            item.horn,
            item.roll & item.air_tail,
            item.wings
          ),

          tech.ground_tail_jump & Any(
            item.high_jump,
          ),

          tech.air_tail_jump & Any(
            item.roll & tech.bubble_jump,
            item.wings & item.high_jump
          )
        )
      )
    ),

    LobbySewerUnderwater: item.swim
  }

@lazy_region
def LobbySewerUnderwater(r: Region):
  r.locations = {
    "Card: Water Lobby - Sewer Bottom": None
  }

  from ..CAVE import Sewer

  r.entrances = [
    SewerDoor.define(Sewer.GalleryDoor)
  ]

  r.region_connections = {
    LobbySewerMiddle: None,
    LobbySewerGiant: None
  }

@lazy_region
def LobbySewerGiant(r: Region):
  r.locations = {
    "Water Lobby - Helped Sniffles": item.bubble | carrying.medicine
  }

  from . import EarthLobby

  r.entrances = [
    GiantDrain.define(EarthLobby.ToiletCoffins)
  ]

  r.region_connections = {
    LobbySewerUnderwater: item.swim
  }

@lazy_region
def LobbySewerEgg(r: Region):
  r.locations = {
    "Egg: Water Lobby - Sewer": Any(
      templates.high_jump_obstacle,
      carrying.jester_boots,
      item.wings,
      carrying.mr_kerringtons_wings,
    )
  }

  from . import EarthLobby

  r.entrances = [
    EggDrain.define(EarthLobby.ToiletPainting)
  ]

  r.region_connections = {
    LobbySewerMiddle: None
  }
