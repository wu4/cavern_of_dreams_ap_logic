from ...logic.objects import EntranceType, InternalEvent
from ...logic import lazy_region, Entrance, Region, CarryableLocation
from ...logic.comment import Comment
from ...logic import item, tech, carrying, difficulty, event
from ...logic import Any

class GreenMedicine(CarryableLocation): carryable = "Medicine"
class MainMedicine(CarryableLocation): carryable = "Medicine"
class SkyDoorFront(Entrance): pass
class SkyDoorBack(Entrance): pass
class SkyDogDoor(Entrance): pass
class SkyFenceDoor(Entrance): pass
class EarthLobbyCauldron(Entrance): pass
class HeartDoor(Entrance): pass

class MainBoils(InternalEvent): pass
class GreenBoil(InternalEvent): pass
class HornOnAnnoyingGenerator(InternalEvent): pass
class CockpitAccess(InternalEvent): pass

CanEnterCockpit = Any(
  tech.any_super_jump,
  event.Collected("Open Armada Cockpit")
)

@lazy_region
def Main(r: Region):
  r.locations = {
    MainMedicine: item.carry,

    MainBoils: carrying.medicine,

    "Kerrington - Soothe Mr. Kerrington's Boils":
      event.Collected(MainBoils) & event.Collected(GreenBoil),

    "Egg: Kerrington - Pipe": None,

    "Card: Kerrington - Pipe": None,

    "Shroom: Kerrington - Pipe Ramp 1": None,
    "Shroom: Kerrington - Pipe Ramp 2": None,
    "Shroom: Kerrington - Pipe Ramp 3": None,

    "Shroom: Kerrington - Pipe 1": None,
    "Shroom: Kerrington - Pipe 2": None,
    "Shroom: Kerrington - Pipe 3": None,
    "Shroom: Kerrington - Pipe 4": None,
    "Shroom: Kerrington - Pipe 5": None,

    "Shroom: Kerrington - Lab Entryway 1": None,
    "Shroom: Kerrington - Lab Entryway 2": None,
    "Shroom: Kerrington - Lab Entryway 3": None,
    "Shroom: Kerrington - Lab Entryway 4": None,

    "Shroom: Kerrington - Hammocks Entryway 1": None,
    "Shroom: Kerrington - Hammocks Entryway 2": None,

    "Shroom: Kerrington - Cockpit Entry 1": None,
    "Shroom: Kerrington - Cockpit Entry 2": None,
    "Shroom: Kerrington - Cockpit Entry 3": None,
    "Shroom: Kerrington - Cockpit Entry 4": None,
    "Shroom: Kerrington - Cockpit Entry 5": None,
    "Shroom: Kerrington - Cockpit Entry 6": None,

    "Card: Kerrington - Hammocks": Any(
      tech.any_super_jump,
      carrying.jester_boots,
      tech.bubble_jump,
      tech.air_tail_jump,
      tech.ground_tail_jump,

      item.double_jump,
      item.wings,
      carrying.mr_kerringtons_wings,
    ),

    "Kerrington - Generators Puzzle": Any(
      item.air_tail | item.ground_tail,
      carrying.apple | carrying.bubble_conch,
      item.horn & event.Collected(HornOnAnnoyingGenerator)
    ),
  }

  r.region_connections = {
    MedicinePool: event.Collected("Open Medicine Pool"),

    Cockpit: CanEnterCockpit,

    HeartEntryway: event.Collected("Open Kerrington's Heart") & Any(
      event.Collected("Free Armada Buddies"),
      carrying.mr_kerringtons_wings,
      carrying.jester_boots,
      tech.super_bubble_jump,
      item.double_jump & Any(
        tech.super_bounce,
        item.air_tail & item.roll
      ),
      tech.bubble_jump & Any(
        tech.super_bounce,
        item.double_jump & Any(
          tech.ground_tail_jump,
          tech.air_tail_jump,
          item.sprint
        )
      ),
      tech.bubble_jump_and_recoil & tech.z_target & Any(
        tech.wing_jump,
        item.horn & item.double_jump
      ),
      item.wings & Any(
        item.double_jump,
        item.horn,
        tech.air_tail_jump,
        tech.ground_tail_jump,
      )
    ),

    IntoFrontDoor: Any(
      tech.any_super_jump,
      item.climb,
      carrying.jester_boots & item.double_jump
    ),

    GreenRoom: Any(
      tech.any_super_jump,
      carrying.jester_boots,
      item.climb,
      item.wings,
      carrying.mr_kerringtons_wings,
      item.double_jump,
      tech.damage_boost & tech.momentum_cancel,
      tech.air_tail_jump,
      tech.ground_tail_jump,
      item.roll & item.sprint,
      tech.bubble_jump,
    ),

    LowerLabContainers: Any(
      item.double_jump & Any(
        item.horn,
        tech.ground_tail_jump,
        carrying.mr_kerringtons_wings,
        Comment(
          "Wing Storage from the medicine pipe",
          tech.wing_jump & tech.wing_storage
        )
      ),

      (
        event.Collected("Free Armada Buddies") &
        (item.swim | difficulty.intermediate) &
        Any(
          tech.ground_tail_jump,
          tech.air_tail_jump & item.high_jump,
          item.horn & Any(
            difficulty.intermediate,
            item.double_jump,
            item.wings
          )
        )
      )
    ),

    UpperLabContainers: Any(
      tech.ability_toggle & item.wings & item.double_jump
    ),

  }

@lazy_region
def IntoFrontDoor(r: Region):
  from . import Sky

  r.entrances = [
    SkyDoorFront.define(Sky.KerringtonDoorFront)
  ]

  r.region_connections = {
    Main: None
  }

@lazy_region
def GreenRoom(r: Region):
  r.locations = {
    GreenMedicine: item.carry,

    GreenBoil: carrying.medicine,

    "Shroom: Kerrington - Rain Entryway 1": None,
    "Shroom: Kerrington - Rain Entryway 2": None,
    "Shroom: Kerrington - Rain Entryway 3": None,
    "Shroom: Kerrington - Rain Entryway 4": None,

    "Shroom: Kerrington - Rain Below Boiler 1": None,
    "Shroom: Kerrington - Rain Below Boiler 2": None,
    "Shroom: Kerrington - Rain Below Boiler 3": None,

    "Shroom: Kerrington - Rain Plant Base": None,
    "Shroom: Kerrington - Rain Plant 1": None,
    "Shroom: Kerrington - Rain Plant 2": None,
    "Shroom: Kerrington - Rain Plant 3": None,
    "Shroom: Kerrington - Rain Plant 4": None,

    "Shroom: Kerrington - Rain Below Medicine 1": None,
    "Shroom: Kerrington - Rain Below Medicine 2": None,
    "Shroom: Kerrington - Rain Below Medicine 3": None,
  }

  r.region_connections = {
    Main: None,
    GreenFence: None,
    LabGreenConnector: Any(
      tech.any_super_jump,
    ),
    GreenBoiler: Any(
      item.wings,
      tech.bubble_jump & (item.high_jump | item.roll),
      item.horn,
      item.double_jump,
      item.roll & item.sprint,
      Comment(
        "Precise jump from the blue bouncy shroom stalk",
        Any(
          tech.air_tail_jump,
          tech.ground_tail_jump
        )
      )
    )
  }

@lazy_region
def GreenBoiler(r: Region):
  r.locations = {
    "Shroom: Kerrington - Rain Above Boiler 1": None,
    "Shroom: Kerrington - Rain Above Boiler 2": None,
    "Shroom: Kerrington - Rain Above Boiler 3": None,
    "Shroom: Kerrington - Rain Above Boiler 4": None,

    "Egg: Kerrington - Boiler": item.swim,
  }

  r.region_connections = {
    Main: None
  }

@lazy_region
def LabGreenConnector(r: Region):
  r.locations = {
    "Shroom: Kerrington - Lab Rain Connector 1": None,
    "Shroom: Kerrington - Lab Rain Connector 2": None,
    "Shroom: Kerrington - Lab Rain Connector 3": None,
    "Shroom: Kerrington - Lab Rain Connector 4": None,
    "Shroom: Kerrington - Lab Rain Connector 5": None,
    "Shroom: Kerrington - Lab Rain Connector 6": None,
  }

  r.region_connections = {
    GreenRoom: None,
    GreenBoiler: None,
    LowerLabContainers: None,
    UpperLabContainers: None
  }

@lazy_region
def LowerLabContainers(r: Region):
  r.locations = {
    HornOnAnnoyingGenerator: item.horn
  }

  r.region_connections = {
    Main: None,
    LabGreenConnector: Any(
      item.climb,
      event.Collected("Free Armada Buddies") & Any(
        item.high_jump & Any(
          tech.air_tail_jump,
          item.double_jump
        ),
        item.horn & Any(
          item.wings,
          item.double_jump
        ),
        tech.ground_tail_jump,
        difficulty.intermediate & item.air_tail & item.roll
      )
    ),

    UpperLabContainers: Any(
      item.double_jump & Any(
        carrying.mr_kerringtons_wings,
        item.wings
      ),

      item.high_jump & Any(
        carrying.mr_kerringtons_wings,
        item.wings & Any(
          tech.air_tail_jump,
          tech.ground_tail_jump
        )
      ),

      event.Collected("Free Armada Buddies") & Any(
        item.double_jump & item.wings
      )
    )
  }

@lazy_region
def UpperLabContainers(r: Region):
  r.region_connections = {
    Main: None,
    LabGreenConnector: Any(
      tech.ground_tail_jump,
      tech.air_tail_jump,

      event.Collected("Free Armada Buddies") & Any(
        item.wings,
        tech.bubble_jump,
      )
    )
  }

@lazy_region
def GreenFence(r: Region):
  from . import Sky

  r.entrances = [
    SkyFenceDoor.define(
      default_connection = Sky.GreenDoor,
      rule = Any(
        item.air_tail | item.ground_tail,
        carrying.apple | carrying.bubble_conch,
        tech.roll_disjoint
      )
    )
  ]

  r.region_connections = {
    GreenRoom: Any(
      tech.any_super_jump,
      carrying.mr_kerringtons_wings,
      item.wings & tech.bubble_jump_and_recoil,
      item.roll & Any(
        item.air_tail,
        item.sprint
      ),
      item.double_jump & Any(
        item.wings,
        item.horn,
        tech.ground_tail_jump,
        tech.air_tail_jump & item.high_jump
      ),
      tech.wing_storage & Any(
        item.high_jump,
        item.sprint
      )
    )
  }

@lazy_region
def MedicinePool(r: Region):
  r.locations = {
    "Shroom: Kerrington - Slide Entryway 1": None,
    "Shroom: Kerrington - Slide Entryway 2": None,
    "Shroom: Kerrington - Slide Entryway 3": None,

    "Kerrington - Medicine Pool Preston": None,
    "Card: Kerrington - Slide": Any(
      tech.wing_jump & Any(
        item.high_jump,
        tech.bubble_jump_and_recoil
      ),
      item.horn & item.double_jump,
      item.air_tail & item.roll,
      tech.ground_tail_jump & Any(
        tech.bubble_jump,
        item.double_jump,
        item.wings,
      ),
      item.wings & Any(
        item.double_jump,
        item.horn,
      )
    ),
  }

  from . import Sky

  r.entrances = [
    SkyDoorBack.define(
      default_connection = Sky.KerringtonDoorBack,
      type = EntranceType.ENTRANCE
    )
  ]

  r.region_connections = {
    Main: event.Collected("Open Medicine Pool"),

    MedicinePoolSlide: Any(
      tech.any_super_jump,
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,

      tech.air_tail_jump,
      tech.ground_tail_jump,
      item.wings,
      item.double_jump,
      item.sprint & item.roll,
      tech.bubble_jump & Any(
        item.sprint,
        item.roll,
        item.horn
      )
    )
  }

@lazy_region
def MedicinePoolSlide(r: Region):
  r.region_connections = {
    MedicinePoolEggPlatform: Any(
      difficulty.intermediate,

      tech.any_super_jump,
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,

      item.high_jump,
      item.sprint,
      item.double_jump,
      tech.bubble_jump,
      item.horn,
      tech.air_tail_jump,
      tech.ground_tail_jump,
      item.wings,
    )
  }

@lazy_region
def MedicinePoolEggPlatform(r: Region):
  r.locations = {
    "Egg: Kerrington - Slide": None
  }

  r.region_connections = {
    MedicinePool: None
  }

@lazy_region
def Cockpit(r: Region):
  r.locations = {
    CockpitAccess: None
  }

  r.region_connections = {
    Main: CanEnterCockpit
  }

@lazy_region
def HeartEntryway(r: Region):
  from . import Heart

  r.entrances = [
    HeartDoor.define(Heart.KerringtonDoor)
  ]

  r.region_connections = {
    Main: event.Collected("Open Kerrington's Heart"),
    HeartEntrywayPlatform: Any(
      item.high_jump,
      tech.ground_tail_jump,
      tech.air_tail_jump,
      item.horn,
      carrying.mr_kerringtons_wings & tech.wing_jump
    ),
    HeartEntrywayCardPlatform: tech.any_super_jump
  }

@lazy_region
def HeartEntrywayPlatform(r: Region):
  r.region_connections = {
    HeartEntryway: None,
    HeartEntrywayCardPlatform: Any(
      carrying.jester_boots,
      carrying.mr_kerringtons_wings,
      item.roll & item.air_tail,
      tech.wing_jump & tech.bubble_jump_and_recoil,
      tech.bubble_jump & item.double_jump & Any(
        item.horn,
        item.sprint,
        tech.air_tail_jump,
        tech.ground_tail_jump
      )
    )
  }

@lazy_region
def HeartEntrywayCardPlatform(r: Region):
  r.locations = {
    "Card: Kerrington - Near Mr. Kerrington's Heart": None
  }

  r.region_connections = {
    HeartEntryway: None
  }

@lazy_region
def DogRoom(r: Region):
  r.locations = {
    "Egg: Kerrington - Dog Food": None
  }

  from . import Sky

  r.entrances = [
    SkyDogDoor.define(Sky.YellowDoor)
  ]

CanOpenCauldronRoom = Any(
  item.ground_tail | item.air_tail,
  carrying.apple | carrying.bubble_conch
)

@lazy_region
def CauldronRoom(r: Region):
  from ..GALLERY import EarthLobby

  r.entrances = [
    EarthLobbyCauldron.define(EarthLobby.KerringtonCauldron)
  ]

  r.region_connections = {
    Main: CanOpenCauldronRoom
  }
