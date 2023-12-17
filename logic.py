from __future__ import annotations
from typing import Literal, TypeAlias
from generated import AnyLocation, abilityItem, nonVanillaAbilityItem, eventItem

class Logic:
  def __and__(self, other: Logic) -> All:
    return All(self, other)

  def __or__(self, other: Logic) -> Any:
    return Any(self, other)
  
class Comment(Logic):
  comment: str
  logic: Logic

  def __str__(self) -> str:
    return f"'{self.comment}' ({self.logic})"

  def __init__(self, comment: str, logic: Logic) -> None:
    super().__init__()
    self.comment = comment
    self.logic = logic

class All(Logic):
  operands: list[Logic]
  
  def __str__(self) -> str:
    return "(" + (" && ".join(map(str, self.operands))) + ")"

  def __init__(self, *args: Logic) -> None:
    super().__init__()
    unwrap: list[Logic] = []
    for item in args:
      if isinstance(item, All):
        unwrap.extend(item.operands)
      else:
        unwrap.append(item)
    self.operands = unwrap

class Any(Logic):
  operands: list[Logic]

  def __str__(self) -> str:
    return "(" + (" || ".join(map(str, self.operands))) + ")"

  def __init__(self, *args: Logic) -> None:
    super().__init__()
    unwrap: list[Logic] = []
    for item in args:
      if isinstance(item, Any):
        unwrap.extend(item.operands)
      else:
        unwrap.append(item)
    self.operands = unwrap

HasType: TypeAlias = abilityItem | nonVanillaAbilityItem

class HasAbility(Logic):
  def __str__(self) -> str:
    return f"Has {self.has}"
  
  def __init__(self, has: HasType) -> None:
    self.has = has
    super().__init__()

class HasEvent(Logic):
  def __str__(self) -> str:
    return f"Triggered {self.event}"
  
  def __init__(self, event: eventItem) -> None:
    self.event = event
    super().__init__()

class HasEggs(Logic):
  def __str__(self) -> str:
    return f"Has at least {self.eggs} eggs"
  
  def __init__(self, eggs: int) -> None:
    self.eggs = eggs
    super().__init__()

class HasHearts(Logic):
  def __str__(self) -> str:
    return f"Has at least {self.hearts} hearts"
  
  def __init__(self, hearts: int) -> None:
    self.hearts = hearts
    super().__init__()

CarryingType: TypeAlias = Literal[
  "Jester Boots",
  "Apple",
  "Potion",
  "Bubble Conch"
]

class Impossible(Logic):
  def __str__(self) -> str:
    return "Impossible"

class DropCarryable(Logic):
  def __str__(self) -> str:
    drop: list[str] = []
    if self.jester_boots: drop.append("Jester Boots")
    if self.throwable: drop.append("Throwables")
    return f"Drop [{', '.join(drop)}] for [{self.logic}]"

  def __init__(self, logic: MaybeLogic, jester_boots: bool = False, throwable: bool = False) -> None:
    self.jester_boots = jester_boots
    self.throwable = throwable
    self.logic = logic
    super().__init__()

class Carrying(Logic):
  def __str__(self) -> str:
    return f"Carrying {self.carrying}"
  
  def __init__(self, carrying: CarryingType) -> None:
    self.carrying = carrying
    super().__init__()
    

TechType: TypeAlias = Literal[
  "ejection_launch",
  "z_target",
  "momentum_cancel",
  "damage_boost",

  "tail_jump",
  "hover_jump",
  "hover_shoot",
  "super_bubble_jump",
  "super_bounce",
  "bubble_jump",
]

class InternalEvent:
  pass

class HasInternalEvent(Logic):
  def __str__(self) -> str:
    return f"(internal) {self.event.__name__}"

  def __init__(self, event: type[InternalEvent]) -> None:
    self.event = event
    super().__init__()

class Tech(Logic):
  def __str__(self) -> str:
    return f"Tech: {self.tech}"
  
  def __init__(self, tech: TechType) -> None:
    self.tech = tech
    super().__init__()

class CanWhack(Logic):
  def __str__(self) -> str:
    accum: list[str] = []
    if self.ground_tail_works: accum.append("Ground Tail")
    if self.air_tail_works: accum.append("Air Tail")
    if self.roll_works: accum.append("Roll")
    if self.throwable_works: accum.append("Throwables")
    if self.horn_works: accum.append("Horn")
    return "Whackable [" + " | ".join(accum) + "]"
  
  def __init__(
    self,
    ground_tail_works: bool = False,
    air_tail_works: bool = False,
    roll_works: bool = False,
    throwable_works: bool = False,
    horn_works: bool = False
  ) -> None:
    self.ground_tail_works = ground_tail_works
    self.air_tail_works = air_tail_works
    self.roll_works = roll_works
    self.throwable_works = throwable_works
    self.horn_works = horn_works
    super().__init__()

DifficultyType: TypeAlias = Literal["Intermediate", "Hard"]

class Difficulty(Logic):
  def __str__(self) -> str:
    return f"Difficulty: {self.difficulty}"
  
  def __init__(self, difficulty: DifficultyType) -> None:
    self.difficulty = difficulty
    super().__init__()

HasWings: Logic = HasAbility("Wings")
HasDoubleJump: Logic = HasAbility("Double Jump")
HasHorn: Logic = HasAbility("Horn")
HasBubble: Logic = HasAbility("Bubble")
HasFlight: Logic = HasAbility("Flight")
HasAirTail: Logic = HasAbility("Aerial Tail")
HasGroundTail: Logic = HasAbility("Grounded Tail")
HasRoll: Logic = HasAbility("Roll")
HasSprint: Logic = HasAbility("Sprint")
HasHighJump: Logic = HasAbility("High Jump")
HasSwim: Logic = HasAbility("Swim")
HasClimb: Logic = HasAbility("Climb")
HasCarry: Logic = HasAbility("Carry")
HasSuperJumps: Logic = HasAbility("Super Jumps")
HasAirSwim: Logic = HasAbility("Air Swim")

CanHoverJump: Logic = Tech("hover_jump") & HasWings
CanBubbleJump: Logic = Tech("bubble_jump") & HasBubble
CanHoverShoot: Logic = Tech("hover_shoot") & HasWings & HasBubble
CanSuperBounce: Logic = Tech("super_bounce") & HasSuperJumps & HasRoll & HasAirTail
CanSuperBubbleJump: Logic = Tech("super_bubble_jump") & HasSuperJumps & HasRoll & HasBubble

def CanTailJump(groundedTail: Logic | None = None, aerialTail: Logic | None = None) -> Logic:
  return Tech("tail_jump") & Any(
    HasGroundTail if groundedTail is None else HasGroundTail & groundedTail,
    HasAirTail if aerialTail is None else HasAirTail & aerialTail,
  )

CanSuperJump = CanSuperBounce | CanSuperBubbleJump

HighJumpObstacle = Any(
  HasHighJump,
  HasHorn,
  HasDoubleJump,
  CanTailJump(),
  CanSuperJump
)

MaybeLogic = Logic | None

class RegionDefinition:
  def __init__(
    self,
    region_connections: dict[type[Region], MaybeLogic] = {},
    entrances: dict[type[Entrance], EntranceDefinition] = {},
    locations: dict[AnyLocation, MaybeLogic] = {}
  ) -> None:
    self.region_connections = region_connections
    self.entrances = entrances
    self.locations = locations

class Region:
  region_connections: dict[type[Region], MaybeLogic]
  entrances: set[type[Entrance]]
  locations: dict[AnyLocation, MaybeLogic]

class EntranceDefinition:
  def __init__(self, to: type[Entrance], rule: MaybeLogic = None) -> None:
    self.to = to
    self.rule = rule
    
class Entrance:
  to: type[Entrance]
  rule: MaybeLogic
  
class Area:
  def __init__(self, regions: dict[type[Region], RegionDefinition]) -> None:
    self.regions: set[type[Region]] = set()
    for k, v in regions.items():
      k.region_connections = v.region_connections
      k.locations = v.locations
      entrances: set[type[Entrance]] = set()
      for kk, vv in v.entrances.items():
        kk.to = vv.to
        kk.rule = vv.rule
        
        entrances.add(kk)

      k.entrances = entrances
      self.regions.add(k)