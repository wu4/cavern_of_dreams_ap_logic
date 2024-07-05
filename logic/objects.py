from __future__ import annotations
from abc import abstractmethod
from enum import Flag

from .has import CarryingItem
from .logic import MaybeLogic as _MaybeLogic
from ..generated_types import AnyLocation

from typing import Callable, TypeAlias, override

class HasPathName:
  @classmethod
  def name(cls) -> str:
    return f"{cls.__module__}.{cls.__name__}"

class InternalEvent(HasPathName):
  @override
  def __str__(self) -> str:
    return f"Has {self.name()}"

class CarryableLocation(InternalEvent):
  carryable: CarryingItem  # pyright: ignore[reportUninitializedInstanceVariable]

class PlantableSoil(InternalEvent): pass


LocationType: TypeAlias = AnyLocation | type[InternalEvent] | type[CarryableLocation]

class Region:
  _is_defined: bool = False
  name: str
  region_connections: dict[Region, _MaybeLogic] | None = None
  entrances: list[type[Entrance]] | None = None
  locations: dict[LocationType, _MaybeLogic] | None = None

  def __init__(self, name: str):
    super().__init__()
    self.name = name

  def lazy_load(self):
    if self._is_defined: return
    self.load()
    self._is_defined = True

  @abstractmethod
  def load(self):
    """
    Overridden by Regions to define attributes that require lazy-loading
    """

def lazy_region(func: Callable[[Region], None]):
  """
  Creates a new Region, using the provided function for its name and lazy-loading.
  """
  r = Region(func.__name__)
  def wrapped():
    func(r)
  r.load = wrapped
  return r

class EntranceType(Flag):
  ENTRANCE   = 0b001
  EXIT       = 0b010
  BILINEAR   = 0b011
  UNDERWATER = 0b100

class Entrance:
  _is_defined: bool = False

  @classmethod
  def set_containing_region(cls, region: type[Region]):
    cls.containing_region = region

  @classmethod
  def define(cls, default_connection: type[Entrance], rule: _MaybeLogic = None, type: EntranceType = EntranceType.BILINEAR) -> type[Entrance]:
    assert not cls._is_defined, f"Tried to redefine {cls.__name__}"
    cls._is_defined = True

    cls.default_connection = default_connection
    cls.rule = rule
    cls.type = type

    return cls
