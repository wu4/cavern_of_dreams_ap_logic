from ...logic import lazy_region, Region, Entrance, InternalEvent, Any, All, CarryableLocation
from ...logic import item, carrying, tech, event, difficulty
from ...logic.comment import Comment

area_path = "GALLERY/Earth Lobby"

class FoyerDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromEarthLobbyToFoyer"
  dest_path = f"{area_path}/Warps/DestFromFoyerToEarthLobby"

class UndeadPainting(Entrance):
  _painting_path = f"{area_path}/Objects (Castle)/PaintingWarpUndead"
  warp_path = f"{_painting_path}/WarpCutscene/WarpEvent"
  dest_path = f"{_painting_path}/DestFromPaintingUndead"

class KerringtonCauldron(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromEarthLobbyToMonster"
  dest_path = f"{area_path}/Warps/DestFromMonsterToEarthLobby"

class FireLobbyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpEarthToFire"
  dest_path = f"{area_path}/Warps/DestFireToEarth"

class ToiletDragonHead(Entrance):
  warp_path = f"{area_path}/Warps/WarpPitMoon"

class ToiletBridge(Entrance):
  warp_path = f"{area_path}/Warps/WarpPitCenter"

class ToiletCoffins(Entrance):
  warp_path = f"{area_path}/Warps/WarpPitLake"

class ToiletPainting(Entrance):
  warp_path = f"{area_path}/Warps/WarpPitNearPainting"

class GrewCastleBushes(InternalEvent): pass
class GrewMainBush(InternalEvent): pass
class KerringtonWings(CarryableLocation): carryable = "Mr. Kerrington's Wings"

class RealignDragonHeadStatue(InternalEvent): pass
class RealignMainStatue(InternalEvent): pass
class RealignCoffinsStatue(InternalEvent): pass
whack_statue = Any(
  item.air_tail, item.ground_tail,
  carrying.apple, carrying.bubble_conch
)

@lazy_region
def GrowMainBush(r: Region):
  r.locations = {
    GrewMainBush: None
  }

@lazy_region
def Main(r: Region):
  r.locations = {
    "Card: Gallery of Nightmares - Swamp Castle": None,
    "Gallery of Nightmares - Shelnert's Painting": carrying.shelnerts_fish,
    "Egg: Gallery of Nightmares - Skull's Eye": event.Collected("Open Skull's Diamond Eye"),
    "Gallery of Nightmares - Swamp Angel Statue Puzzle": All(
      event.Collected(RealignMainStatue),
      event.Collected(RealignDragonHeadStatue),
      event.Collected(RealignCoffinsStatue)
    ),

    RealignMainStatue: whack_statue,
  }

  r.region_connections = {
    MainUnderwater: item.swim,

    InsideCastle: event.Collected("Open Gallery of Nightmares Swamp Door"),

    GrowMainBush: item.bubble | carrying.medicine,

    DragonHead: Any(
      item.double_jump,
      tech.ground_tail_jump,
      tech.air_tail_jump,
      (item.high_jump | item.horn) & tech.bubble_jump,
      item.wings,
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
    ),

    Coffins: Any(
      event.Collected(GrewMainBush),
      tech.any_super_jump,
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      item.double_jump,
      item.wings,
      tech.ground_tail_jump,
      tech.air_tail_jump,
    ),

    FoyerEntryPlatform: Any(
      tech.any_super_jump,
      item.climb,
      carrying.jester_boots,
      item.high_jump & item.double_jump & item.sprint & carrying.mr_kerringtons_wings,
      tech.wing_jump & tech.bubble_jump_and_recoil & tech.ability_toggle & tech.z_target & item.horn & item.double_jump
    )
  }

@lazy_region
def MainUnderwater(r: Region):
  r.locations = {
    "Card: Gallery of Nightmares - Swamp": None
  }

  from . import WaterLobby

  r.entrances = [
    ToiletBridge.define(WaterLobby.CenterDrain),
    ToiletDragonHead.define(WaterLobby.FarDrain)
  ]

  r.region_connections = {
    Main: None,
    Coffins: None
  }

@lazy_region
def FoyerEntryPlatform(r: Region):
  from . import Foyer

  r.entrances = [
    FoyerDoor.define(Foyer.EarthLobbyDoor)
  ]

  r.region_connections = {
    Main: None
  }

coffins_jump = Any(
  tech.air_tail_jump,
  tech.ground_tail_jump,
  item.wings,
  tech.bubble_jump,
  item.double_jump,
)

@lazy_region
def Coffins(r: Region):
  r.region_connections = {
    GrowMainBush: item.bubble | carrying.medicine,
    MainUnderwater: item.swim,
    CoffinsUnderwater: item.swim,

    CoffinsStatuePlatform: coffins_jump,

    FireLobbyEntryway: Any(
      tech.any_super_jump,
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
      item.wings & Any(
        item.double_jump,
        item.horn,
        item.high_jump & tech.wing_jump
      ),
      item.air_tail & item.roll & difficulty.intermediate,
      tech.ground_tail_jump & item.double_jump & (difficulty.intermediate | item.high_jump),
      tech.air_tail_jump & item.double_jump & item.high_jump
    ),

    Main: Any(
      event.Collected(GrewMainBush),
      tech.any_super_jump,
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      item.double_jump,
      item.wings,
      tech.ground_tail_jump,
      tech.air_tail_jump,

      item.sprint,
      Comment(
        "Roll from the ledge, then dive to reset vertical momentum",
        item.roll & item.horn
      )
    )
  }

@lazy_region
def CoffinsStatuePlatform(r: Region):
  r.locations = {
    RealignCoffinsStatue: whack_statue
  }

  r.region_connections = {
    CoffinsUnderwater: item.swim,
    Coffins: coffins_jump
  }

@lazy_region
def CoffinsUnderwater(r: Region):
  from . import WaterLobby

  r.entrances = [
    ToiletCoffins.define(WaterLobby.GiantDrain)
  ]

  r.region_connections = {
    Coffins: None
  }

@lazy_region
def DragonHead(r: Region):
  r.locations = {
    RealignDragonHeadStatue: whack_statue
  }

  r.region_connections = {
    MainUnderwater: item.swim,
    Main: Any(
      item.double_jump,
      tech.ground_tail_jump,
      tech.air_tail_jump,
      (item.high_jump | item.horn) & tech.bubble_jump,
      item.wings,
      carrying.mr_kerringtons_wings,
      carrying.jester_boots
    )
  }

@lazy_region
def FireLobbyEntryway(r: Region):
  from . import FireLobby

  r.entrances = [
    FireLobbyDoor.define(FireLobby.EarthLobbyDoor)
  ]

  r.region_connections = {
    Coffins: None
  }

@lazy_region
def GrowCastleBushes(r: Region):
  r.locations = {
    GrewCastleBushes: None
  }

@lazy_region
def CastleUnderwater(r: Region):
  from . import WaterLobby

  r.entrances = [
    ToiletPainting.define(WaterLobby.EggDrain)
  ]

  r.region_connections = {
    InsideCastle: None
  }

@lazy_region
def InsideCastle(r: Region):
  r.locations = {
    "Gallery of Nightmares - Moisten Wastes of Eternity Painting": item.bubble
  }

  from . import Undead

  r.entrances = [
    UndeadPainting.define(Undead.EarthLobbyDoor)
  ]

  r.region_connections = {
    GrowCastleBushes: item.bubble | carrying.medicine,
    Main: event.Collected("Open Gallery of Nightmares Swamp Door"),
    CastleUnderwater: item.swim,
    CastleWingsPlatform: Any(
      event.Collected(GrewCastleBushes),
      tech.any_super_jump,
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      item.wings,
      item.double_jump,
      tech.ground_tail_jump,
      tech.air_tail_jump,
      item.horn,
    )
  }

@lazy_region
def CastleWingsPlatform(r: Region):
  r.locations = {
    KerringtonWings: item.carry
  }

  r.region_connections = {
    InsideCastle: None
  }

@lazy_region
def KerringtonCauldronPlatform(r: Region):
  r.locations = {
    "Gallery-Armada Connector - Preston": None
  }

  r.region_connections = {
    InsideCastle: None,
    KerringtonCauldronEntryway: event.Collected("Open Gallery-Armada Connector")
  }

@lazy_region
def KerringtonCauldronEntryway(r: Region):
  from ..MONSTER import Kerrington

  r.entrances = [
    KerringtonCauldron.define(Kerrington.EarthLobbyCauldron)
  ]

  r.region_connections = {
    KerringtonCauldronPlatform: event.Collected("Open Gallery-Armada Connector")
  }
