from typing import Callable, TypeAlias
from .type import CollectionState

ConnectionRuleFactory: TypeAlias = Callable[["RulesContext"], Callable[[CollectionState], bool]]
RulesDict: TypeAlias = dict[str, ConnectionRuleFactory | None]

class Entrance:
  to: tuple[str, str]
  rule: ConnectionRuleFactory | None
  def __init__(self, to: tuple[str, str], rule: ConnectionRuleFactory | None = None) -> None:
    self.to = to
    self.rule = rule

class Locations:
  eggs: RulesDict
  events: RulesDict
  cards: RulesDict
  shrooms: RulesDict
  abilities: RulesDict
  def __init__(
    self,
    eggs: RulesDict | None = None,
    events: RulesDict | None = None,
    cards: RulesDict | None = None,
    shrooms: RulesDict | None = None,
    abilities: RulesDict | None = None
  ) -> None:
    self.eggs = eggs if eggs else {}
    self.events = events if events else {}
    self.cards = cards if cards else {}
    self.shrooms = shrooms if shrooms else {}
    self.abilities = abilities if abilities else {}

class Area:
  area_connections: dict[str, ConnectionRuleFactory | None] | None
  entrances: dict[str, Entrance] | None
  locations: Locations | None
  def __init__(
    self,
    area_connections: dict[str, ConnectionRuleFactory | None] | None = None,
    entrances: dict[str, Entrance] | None = None,
    locations: Locations | None = None
  ) -> None:
    self.area_connections = area_connections
    self.entrances = entrances
    self.locations = locations

def shrooms(shroom_base_name: str, shroom_count: int, rule: ConnectionRuleFactory | None = None) -> dict[str, ConnectionRuleFactory | None]:
  return {
    f"{shroom_base_name} {n+1}": rule
    for n in range(shroom_count)
  }

class RulesContext:
    world: World
    player: int
    options: Options

    def __init__(self, world: World) -> None:
        self.player = world.player
        options: Options = world.options
        self.options = options

        if options.dive_without_tailwhip.value > 0:
            self.has_dive = lambda s: s.has("Dive", self.player)
        else:
            self.has_dive = lambda s: s.has("Attack", self.player) and s.has("Dive", self.player)

        if options.shuffle_swim.value > 0:
            self.has_swim = lambda s: s.has("Swim", self.player)
        else:
            self.has_swim = lambda s: True

        if options.shuffle_high_jump.value > 0:
            self.has_high_jump = lambda s: s.has("High Jump", self.player)
        else:
            self.has_high_jump = lambda s: True

        match options.shuffle_roll.value:
            # start with roll
            case 0:
                self.has_roll = lambda s: True
                self.has_fast_roll = self.has_roll

            # shuffle
            case 1:
                self.has_roll = lambda s: s.has("Roll", self.player)
                self.has_fast_roll = self.has_roll

            # progressive shuffle
            case 2: 
                self.has_roll = lambda s: s.has("Roll", self.player)
                self.has_fast_roll = lambda s: s.has("Roll", self.player, 2)

        if options.shuffle_hearts.value > 0:
            self.has_hearts = lambda s, n: s.has("Heart", n)
        else:
            self.has_hearts = lambda s, n: self.has_attack(s) and self.count_teleport_eggs(s) >= n

        if options.hitlaunch_cancels.value > 0:
            self.can_hitlaunch_cancel = lambda s: True
        else:
            self.can_hitlaunch_cancel = lambda s: False

        if options.super_bounce.value > 0:
            self.can_super_bounce = lambda s: self.has_attack(s) and self.has_roll(s)
        else:
            self.can_super_bounce = lambda s: False

        if options.jester_boots_anywhere.value > 0:
            self.can_smuggle_jester_boots = lambda s: s.has("Jester Boots Anywhere Access", self.player)
        else:
            self.can_smuggle_jester_boots = lambda s: False


        
    
    def has_attack(self, s: CollectionState) -> bool:
        return s.has("Attack", self.player)

    def has_wings(self, s: CollectionState) -> bool:
        return s.has("Wings", self.player)

    def has_dive(self, s: CollectionState) -> bool: assert False

    def has_bubble(self, s: CollectionState) -> bool:
        return s.has("Bubble", self.player)

    def has_flight(self, s: CollectionState) -> bool:
        return s.has("Wings", self.player) and s.has("Flight", self.player)

    def has_swim(self, s: CollectionState) -> bool: assert False

    def has_high_jump(self, s: CollectionState) -> bool: assert False

    def has_roll(self, s: CollectionState) -> bool: assert False

    def has_fast_roll(self, s: CollectionState) -> bool: assert False

    def count_teleport_eggs(self, s: CollectionState) -> int:
        return sum(map(lambda i: 1 if s.has(i, self.player) else 0, ["Lostleaf Teleport Egg", "Prismic Teleport Egg", "Armada Teleport Egg", "Gallery Teleport Egg"]))

    def has_hearts(self, s: CollectionState, n: int) -> bool: assert False

    def count_total_eggs(self, s: CollectionState) -> int:
        return s.count("Egg", self.player) + self.count_teleport_eggs(s)

    def has_eggs(self, s: CollectionState, n: int):
        return self.count_total_eggs(s) >= n


    def can_clear_high_jump_obstacle(self, s: CollectionState) -> bool:
        return (
            self.can_bubble_jump(s)
            or self.can_super_bounce(s)
            or self.has_high_jump(s)
            
            or self.has_flight(s)
        )
    def can_clear_whackable(
        self, s: CollectionState,
        attack_works: bool = False,
        roll_works: bool = False,
        throw_works: bool = False,
        dive_works: bool = False,
        projectile_works: bool = False,
        cutscene_works: bool = False
    ):
        return (
            (attack_works and self.has_attack(s))
            or (roll_works and self.has_roll(s) and self.has_attack(s))
            or (throw_works and self.can_smuggle_throwable(s))
            or (dive_works and self.has_dive(s))
            or (projectile_works and self.has_bubble(s))
        )

    def can_douse_flames(self, s: CollectionState) -> bool:
        return self.can_smuggle_medicine(s) or self.has_bubble(s)

    def can_smuggle_throwable(self, s: CollectionState) -> bool:
        return s.has("Apples Access", self.player) or s.has("Bubble Conch Access", self.player)

    def can_smuggle_medicine(self, s: CollectionState) -> bool:
        return s.has("Medicine Access", self.player)

    def can_hitlaunch_cancel(self, s: CollectionState) -> bool: assert False

    def can_super_bounce(self, s: CollectionState) -> bool: assert False

    def can_smuggle_jester_boots(self, s: CollectionState) -> bool: assert False

    def can_bubble_jump(self, s: CollectionState) -> bool:
        return s.has("Bubble", self.player) and self.has_roll(s)
