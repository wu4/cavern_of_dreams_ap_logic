from ...logic import lazy_region, Entrance, Region, Any
from ...logic import item, tech, carrying, templates
from ...logic.comment import Comment

area_path = "MONSTER/Sky (Main)"

class EarthDroneDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromSkyToDroneEarth"
  dest_path = f"{area_path}/Warps/DestFromDroneEarthToSky"
class FireDroneDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromSkyToDroneFire"
  dest_path = f"{area_path}/Warps/DestFromDroneFireToSky"
class WaterDroneDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromSkyToDroneWater"
  dest_path = f"{area_path}/Warps/DestFromDroneWaterToSky"

class KerringtonDoorFront(Entrance):
  warp_path = f"{area_path}/Monster/Warps/WarpFromMonsterToInteriorHead"
  dest_path = f"{area_path}/Monster/Warps/DestFromInteriorToMonsterHead"
class KerringtonDoorBack(Entrance):
  warp_path = f"{area_path}/Monster/Warps/WarpFromMonsterToInteriorTail"
  dest_path = f"{area_path}/Monster/Warps/DestFromInteriorToMonsterTail"
class YellowDoor(Entrance):
  warp_path = f"{area_path}/Monster/Warps/WarpFromMonsterToStorageRoom"
  dest_path = f"{area_path}/Monster/Warps/DestFromStorageRoomToSky"
class GreenDoor(Entrance):
  warp_path = f"{area_path}/Monster/Warps/WarpFromMonsterToGardenRoom"
  dest_path = f"{area_path}/Monster/Warps/DestFromGardenRoomToSky"

# class SkyKerringtonWings(CarryableLocation):
#   location_name = "Airborne Armada - Mr. Kerrington's Wings"
#   carryable = "Mr. Kerrington's Wings"

@lazy_region
def Main(r: Region):
  r.locations = {
    "Shroom: Airborne Armada - Entry Pathway 1": None,
    "Shroom: Airborne Armada - Entry Pathway 2": None,
    "Shroom: Airborne Armada - Entry Pathway 3": None,
    "Shroom: Airborne Armada - Entry Pathway 4": None,
    "Shroom: Airborne Armada - Entry Pathway 5": None,

    "Shroom: Airborne Armada - Front Entrance 1": None,
    "Shroom: Airborne Armada - Front Entrance 2": None,
    "Shroom: Airborne Armada - Front Entrance 3": None,

    "Shroom: Airborne Armada - Side 1": None,
    "Shroom: Airborne Armada - Side 2": None,

    "Card: Airborne Armada - Behind Entry Drone": Any(
      carrying.mr_kerringtons_wings,
      templates.high_jump_obstacle
    )
  }

  from . import EarthDrone, Kerrington

  r.entrances = [
    EarthDroneDoor.define(EarthDrone.SkyDoor),

    KerringtonDoorFront.define(Kerrington.SkyDoorFront)
  ]

  r.region_connections = {
    YellowLedge: Any(
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
      item.air_tail,
      tech.ground_tail_jump,
      item.wings,
      item.roll,
      item.horn,
      item.double_jump,
      item.sprint,
      tech.bubble_jump,
    ),

    GreenDoorway: Any(
      item.air_tail | item.ground_tail,
      carrying.apple | carrying.bubble_conch
    ),

    Topside: Any(
      item.climb,
      tech.any_super_jump,
      Comment(
        "Leap from Mr. Kerrington's eye onto their eyebrow",
        Any(
          item.wings,
          carrying.mr_kerringtons_wings,
          tech.air_tail_jump,
          tech.ground_tail_jump,
          tech.bubble_jump & Any(
            item.horn,
            item.double_jump,
            item.high_jump,
            item.roll
          )
        )
      )
    )
  }

@lazy_region
def YellowLedge(r: Region):
  r.locations = {
    "Shroom: Airborne Armada - Side Yellow Ledge": None
  }

  r.region_connections = {
    YellowDoorway: Any(
      item.air_tail | item.ground_tail,
      carrying.apple | carrying.bubble_conch
    ),

    # jump to the wing
    Main: None,

    Tail: Any(
      carrying.jester_boots,
      item.wings,
      carrying.mr_kerringtons_wings,

      tech.ground_tail_jump,
      tech.air_tail_jump,
      item.roll,
      item.double_jump,
      item.sprint,
      item.horn
    )
  }

@lazy_region
def YellowDoorway(r: Region):
  from . import Kerrington

  r.entrances = [
    YellowDoor.define(Kerrington.SkyDogDoor)
  ]

  r.region_connections = {
    YellowLedge: None
  }

@lazy_region
def GreenDoorway(r: Region):
  from . import Kerrington

  r.entrances = [
    GreenDoor.define(Kerrington.SkyFenceDoor)
  ]

  r.region_connections = {
    Main: None
  }

@lazy_region
def Tail(r: Region):
  r.locations = {
    "Shroom: Airborne Armada - Back Entrance 1": None,
    "Shroom: Airborne Armada - Back Entrance 2": None,
    "Shroom: Airborne Armada - Back Entrance 3": None,
    "Shroom: Airborne Armada - Back Entrance 4": None,
    "Shroom: Airborne Armada - Back Entrance 5": None,
    "Shroom: Airborne Armada - Back Entrance 6": None,

    "Egg: Airborne Armada - Mr. Kerrington's Tail": None
  }

  from . import Kerrington

  r.entrances = [
    KerringtonDoorBack.define(Kerrington.SkyDoorBack)
  ]

  r.region_connections = {
    Topside: Any(
      item.horn,
      tech.ground_tail_jump,
      tech.air_tail_jump,
      tech.bubble_jump,
      item.wings,
      item.sprint,
      item.roll,
      item.high_jump
    )
  }

@lazy_region
def Topside(r: Region):
  r.locations = {
    "Shroom: Airborne Armada - Topside 1": None,
    "Shroom: Airborne Armada - Topside 2": None,
    "Shroom: Airborne Armada - Topside 3": None,

    "Shroom: Airborne Armada - Bouncy Shroom 1": None,
    "Shroom: Airborne Armada - Bouncy Shroom 2": None,
    "Shroom: Airborne Armada - Bouncy Shroom 3": None,
    "Shroom: Airborne Armada - Bouncy Shroom 4": None,
  }

  r.region_connections = {
    Main: None,
    Tail: None,
    YellowLedge: None,
    FireDronePlatform: Any(
      item.wings,
      carrying.mr_kerringtons_wings
    ),
    UpperWings: Any(
      carrying.jester_boots,

      item.wings,
      carrying.mr_kerringtons_wings,
      tech.ground_tail_jump,
      tech.air_tail_jump,
      item.horn,
      tech.bubble_jump & Any(
        item.roll,
        item.high_jump,
        item.sprint
      ),
      item.sprint & Any(
        item.roll,
        item.high_jump
      )
    ),
    WaterDronePlatform: item.sprint & carrying.mr_kerringtons_wings
  }

@lazy_region
def UpperWings(r: Region):
  r.locations = {
    "Card: Airborne Armada - Broken Wing": None
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def FireDronePlatform(r: Region):
  from . import FireDrone

  r.entrances = [
    FireDroneDoor.define(FireDrone.SkyDoor)
  ]

  r.region_connections = {
    Main: None,

    Tail: Any(
      item.wings,

      (item.air_tail | item.sprint) & item.roll & tech.bubble_jump
    )
  }

@lazy_region
def WaterDronePlatform(r: Region):
  r.locations = {
    "Airborne Armada - Mr. Kerrington's Wings": None
  }

  from . import WaterDrone

  r.entrances = [
    WaterDroneDoor.define(WaterDrone.SkyDoor)
  ]

  r.region_connections = {
    Main: item.sprint & carrying.mr_kerringtons_wings
  }
