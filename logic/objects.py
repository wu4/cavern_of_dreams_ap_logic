from __future__ import annotations
from abc import abstractmethod
from types import ModuleType

from .has import CarryingItem
from .logic import MaybeLogic as _MaybeLogic
from ..generated_types import AnyLocation

from typing import Callable, Literal, TypeAlias, override

class HasPathName:
  @classmethod
  def name(cls) -> str:
    return f"{cls.__module__}.{cls.__name__}"

class InternalEvent(HasPathName):
  @override
  def __str__(self) -> str:
    return f"Has {self.name()}"

WhackableRule: TypeAlias = _MaybeLogic | Literal[False]

class Whackable(InternalEvent):
  ground_tail_works: bool = False
  air_tail_works: bool = False
  horn_works: bool = False
  bubble_works: bool = False
  throwables_work: bool = False
  custom_rule: _MaybeLogic = None

  whackable_region: Region | None = None

  @classmethod
  def create_whackable_region(cls) -> Region:
    from .logic import Logic, Any
    from .item import air_tail, ground_tail, horn, bubble
    from .carrying import bubble_conch, apple

    r = Region(f"{cls.name()}.WhackableRegion")
    total_logic: list[Logic] = []
    if cls.ground_tail_works: total_logic.append(ground_tail)
    if cls.bubble_works: total_logic.append(bubble)
    if cls.air_tail_works: total_logic.append(air_tail)
    if cls.horn_works: total_logic.append(horn)

    if cls.throwables_work:
      total_logic.append(bubble_conch)
      total_logic.append(apple)

    if cls.custom_rule is not None:
      total_logic.append(cls.custom_rule)

    r.locations = {
      cls: Any(*total_logic)
    }

    return r

  @classmethod
  def get_whackable_region(cls) -> Region:
    if cls.whackable_region is None:
      cls.whackable_region = cls.create_whackable_region()

    return cls.whackable_region

  @classmethod
  def connecting_to(cls, r: Region) -> dict[Region, _MaybeLogic]:
    from . import event
    return {
      cls.get_whackable_region(): None,
      r: event.Collected(cls)
    }

  @override
  def __str__(self) -> str:
    return f"Whacked {self.name()}"

class CarryableLocation(InternalEvent):
  carryable: CarryingItem  # pyright: ignore[reportUninitializedInstanceVariable]

class PlantableSoil(InternalEvent): pass


LocationType: TypeAlias = AnyLocation | type[InternalEvent] | type[CarryableLocation]

class Region:
  _is_defined: bool = False
  name: str
  region_connections: dict[Region, _MaybeLogic]
  entrances: list[type[Entrance]]
  locations: dict[LocationType, _MaybeLogic]

  def __init__(self, name: str):
    super().__init__()
    self.name = name
    self.region_connections = {}
    self.entrances = []
    self.locations = {}

  def lazy_load(self):
    if self._is_defined: return
    self._is_defined = True
    print(f"loading {self.name}")
    self.load()
    for entrance in self.entrances:
      entrance.set_containing_region(self)

    from inspect import getmodule
    for entrance in self.entrances:
      mod = getmodule(entrance.default_connection)
      if mod is not None and mod not in loaded_modules:
        loaded_modules.add(mod)
        for k, v in mod.__dict__.items():
          if isinstance(v, Region):
            v.lazy_load()

  @abstractmethod
  def load(self):
    """
    Overridden by Regions to define attributes that require lazy-loading
    """

def lazy_region(func: Callable[[Region], None]):
  """
  Creates a new Region, using the provided function for its name and lazy-loading.
  """
  r = Region(f"{".".join(func.__module__.split(".")[-2:])}.{func.__name__}")
  def wrapped():
    func(r)
  r.load = wrapped
  return r

loaded_modules: set[ModuleType] = set()

class Entrance:
  is_dest_underwater: bool = False
  warp_path: str | None = None
  dest_path: str | None = None

  _is_defined: bool = False

  @classmethod
  def set_containing_region(cls, region: Region):
    cls.containing_region = region

  @classmethod
  def define(cls, default_connection: type[Entrance], rule: _MaybeLogic = None) -> type[Entrance]:
    assert not cls._is_defined, f"Tried to redefine {cls.__name__}"
    cls._is_defined = True

    cls.rule = rule

    cls.default_connection = default_connection

    return cls
