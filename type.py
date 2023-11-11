from typing import TypeAlias, Callable, Any, TYPE_CHECKING

class CollectionState:
    def has(self, item: str, player: int, amount: int = 1) -> bool: ...
    def count(self, item: str, player: int) -> int: ...

class HasValue:
    value: int

class Options:
    dive_without_tailwhip: HasValue
    shuffle_swim: HasValue
    shuffle_high_jump: HasValue
    shuffle_roll: HasValue
    shuffle_hearts: HasValue
    hitlaunch_cancels: HasValue
    super_bounce: HasValue
    jester_boots_anywhere: HasValue
    shroomsanity: HasValue
    cardsanity: HasValue

class World:
    player: int
    options: Options

ConnectionRule: TypeAlias = Callable[[CollectionState], bool]