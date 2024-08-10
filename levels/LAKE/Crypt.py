from ...logic.objects import InternalEvent, Whackable
from ...logic import lazy_region, Region, Entrance, Any
from ...logic.comment import Comment
from ...logic import item, difficulty, tech, carrying, event

area_path = "LAKE/Crypt"

class LostleafLakeDoorFront(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromCryptToLake"
  dest_path = f"{area_path}/Warps/DestFromLakeToCrypt"
class LostleafLakeDoorBack(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromCryptToLakeCliff"
  dest_path = f"{area_path}/Warps/DestFromLakeCliffToCrypt"

class PrestonAccess(InternalEvent): pass
class OutOfBounds(InternalEvent): pass

class PrestonDoor(Whackable):
  air_tail_works = True
  ground_tail_works = True
  throwables_work = True

class SecretBackDoor(InternalEvent): pass

class BackDoor(Whackable):
  air_tail_works = True
  ground_tail_works = True
  throwables_work = True
  custom_rule = event.Collected(SecretBackDoor)

class BrokeBackExitWithHorn(InternalEvent): pass

CanBreakBackExit = Any(
  item.air_tail | item.ground_tail,
  carrying.apple | carrying.bubble_conch,
  event.Collected(BrokeBackExitWithHorn)
)

@lazy_region
def Main(r: Region):
  from . import LostleafLake

  r.entrances = [
    LostleafLakeDoorFront.define(
      default_connection = LostleafLake.CryptDoorFront
    )
  ]

  r.region_connections = {
    **PrestonDoor.connecting_to(PrestonRoom),

    RightPlatform: Any(
      carrying.jester_boots,
      tech.any_super_jump,
      item.climb,
      item.horn,
      item.double_jump,
      tech.ground_tail_jump,
      tech.air_tail_jump,
      item.high_jump & Any(difficulty.intermediate, item.wings, tech.bubble_jump),
      tech.wing_storage
    ),

    LeftPlatform: Any(
      item.climb,
      item.wings & tech.bubble_jump_and_recoil,
      tech.any_super_jump,
      item.double_jump & Any(
        item.horn,
        item.high_jump
      ),
      (item.double_jump | item.high_jump) & item.bubble & tech.ground_tail_jump
    )
  }

@lazy_region
def LeftPlatform(r: Region):
  r.region_connections = {
    Main: None,

    **BackDoor.connecting_to(BackExit),

    EggPlatform: Any(
      item.climb,
      item.wings,
      item.double_jump,
      item.horn,
      item.roll,
      item.sprint,
      item.air_tail,
      tech.ground_tail_jump,
      tech.bubble_jump
    ),

    TimedPlatform: event.Collected(PrestonAccess)
  }

@lazy_region
def RightPlatform(r: Region):
  r.region_connections = {
    EggPlatform: Any(
      tech.any_super_jump,

      carrying.jester_boots,
    ),

    TimedPlatform: event.Collected(PrestonAccess) & Any(
      tech.any_super_jump,

      carrying.jester_boots,

      item.high_jump & item.double_jump,
      tech.ground_tail_jump,
      tech.air_tail_jump,

      item.horn,
      item.wings
    )
  }

@lazy_region
def TimedPlatform(r: Region):
  r.region_connections = {
    EggPlatform: None,
    LeftPlatform: None,
    RightPlatform: None,
    Main: None
  }

@lazy_region
def SecretWorld(r: Region):
  r.locations = {
    SecretBackDoor: Comment(
      "Precisely fall onto the block with a dive",
      difficulty.hard & item.horn & Any(item.wings, tech.bubble_jump) & tech.out_of_bounds & tech.ejection_launch & tech.damage_boost & tech.z_target
    ),
  }

  r.region_connections = {
    BackExit: None
  }

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

  r.region_connections = {
    TimedPlatform: event.Collected(PrestonAccess),

    LeftPlatform: Any(
      item.climb,
      item.wings,
      item.double_jump,
      item.horn,
      item.sprint,
      item.air_tail,
      tech.ground_tail_jump,
      tech.bubble_jump
    ),

    SecretWorld: tech.out_of_bounds & tech.ejection_launch & tech.damage_boost & tech.z_target & Any(
      difficulty.intermediate & tech.momentum_cancel & item.double_jump & (item.wings | tech.bubble_jump),

      difficulty.hard & Any(
        item.high_jump,
        item.double_jump,
        item.horn
      )
    )
  }

@lazy_region
def BackExit(r: Region):
  from . import LostleafLake

  r.entrances = [
    LostleafLakeDoorBack.define(
      default_connection = LostleafLake.CryptDoorBack
    )
  ]

  r.region_connections = BackDoor.connecting_to(LeftPlatform)

@lazy_region
def PrestonRoom(r: Region):
  r.locations = {
    PrestonAccess: None
  }

  r.region_connections = PrestonDoor.connecting_to(Main)
