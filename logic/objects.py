from __future__ import annotations
from abc import abstractmethod
from enum import Flag

from .has import CarryingItem
from .logic import MaybeLogic as _MaybeLogic
from ..generated_types import AnyLocation

from typing import TypeAlias, override

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
  region_connections: dict[type[Region], _MaybeLogic] | None = None
  entrances: list[type[Entrance]] | None = None
  locations: dict[LocationType, _MaybeLogic] | None = None

  @classmethod
  def lazy_load(cls):
    if cls._is_defined: return
    cls.load()
    cls._is_defined = True

  @abstractmethod
  @classmethod
  def load(cls):
    """
    Overridden by Regions to define attributes that require lazy-loading
    """

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
