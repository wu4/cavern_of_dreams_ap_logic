from __future__ import annotations
from abc import abstractmethod

from .logic import All, Logic, MaybeLogic as _MaybeLogic
from ..generated_types import AnyLocation

from typing import Callable, Literal, TypeAlias, override

class PathNameMeta(type):
  @override
  def __str__(cls) -> str:
    return f"{'.'.join(cls.__module__.split(".")[-2:])}.{cls.__name__}"

class HasPathName(metaclass=PathNameMeta):
  pass

class InternalEvent(HasPathName):
  pass

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
    from .logic import Any
    from .item import air_tail, ground_tail, horn, bubble
    from .carrying import bubble_conch, apple

    r = Region(f"{str(cls)}.WhackableRegion")
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

# class CarryableLocation(InternalEvent):
#   location_name: str
#   carryable: CarryingItem

class PlantableSoil(InternalEvent):
  soil_region: Region | None = None

  @classmethod
  def create_soil_region(cls) -> Region:
    from .carrying import apple

    r = Region(f"{str(cls)}.PlantableSoil")

    r.locations = {
      cls: apple
    }

    return r

  @classmethod
  def get_soil_region(cls) -> Region:
    if cls.soil_region is None:
      cls.soil_region = cls.create_soil_region()

    return cls.soil_region

  @classmethod
  def climb_rule(cls, additional_climb_rules: _MaybeLogic = None) -> Logic:
    from .event import Collected
    from .item import tree_climb
    climb_rules: list[Logic] = [Collected(cls), tree_climb]
    if additional_climb_rules is not None:
      climb_rules.append(additional_climb_rules)
    return All(*climb_rules)

  @classmethod
  def connecting_to(cls, r: Region, additional_climb_rules: _MaybeLogic = None) -> dict[Region, _MaybeLogic]:
    return {
      cls.get_soil_region(): None,
      r: cls.climb_rule(additional_climb_rules)
    }


LocationType: TypeAlias = AnyLocation | type[InternalEvent]

class Region:
  _is_defined: bool = False
  name: str
  region_connections: dict[Region, _MaybeLogic]
  entrances: list[type[Entrance]]
  locations: dict[LocationType, _MaybeLogic]
  unreachable_if_no_carry_through_doors: bool = False

  def __init__(self, name: str):
    super().__init__()
    self.name = name
    self.region_connections = {}
    self.entrances = []
    self.locations = {}

  def lazy_load(self):
    if self._is_defined: return
    self._is_defined = True
    self.load()
    for entrance in self.entrances:
      entrance.set_containing_region(self)

  @abstractmethod
  def load(self):
    """
    Overridden by Regions to define attributes that require lazy-loading
    """

def module_path(modname: str, name: str) -> str:
  return f"{".".join(modname.split(".")[-2:])}.{name}"

def lazy_region(func: Callable[[Region], None]):
  """
  Creates a new Region, using the provided function for its name and lazy-loading.
  """
  r = Region(module_path(func.__module__, func.__name__))
  def wrapped():
    func(r)
  r.load = wrapped
  return r

class Entrance:
  is_dest_underwater: bool = False
  warp_path: str | None = None
  dest_path: str | None = None

  _is_defined: bool = False

  @classmethod
  def name(cls):
    return module_path(cls.__module__, cls.__name__)

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
