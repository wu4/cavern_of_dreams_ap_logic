from __future__ import annotations
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

  @classmethod
  def define(
    cls,
    region_connections: dict[type[Region], _MaybeLogic] | None = None,
    entrances: list[type[Entrance]] | None = None,
    locations: dict[LocationType, _MaybeLogic] | None = None
  ) -> type[Region]:
    assert not cls._is_defined, f"Tried to redefine {cls.__name__}"

    if region_connections is None: region_connections = {}
    if entrances is None: entrances = []
    if locations is None: locations = {}

    cls._is_defined = True

    cls.region_connections = region_connections
    cls.entrances = entrances
    cls.locations = locations
    for entrance in entrances:
      entrance.set_containing_region(cls)

    return cls

class EntranceType(Flag):
  ENTRANCE = 0b01
  EXIT = 0b10

class Entrance:
  _is_defined: bool = False

  @classmethod
  def set_containing_region(cls, region: type[Region]):
    cls.containing_region = region

  @classmethod
  def define(cls, default_connection: type[Entrance], rule: _MaybeLogic = None, type: EntranceType = EntranceType.ENTRANCE | EntranceType.EXIT) -> type[Entrance]:
    assert not cls._is_defined, f"Tried to redefine {cls.__name__}"
    cls._is_defined = True

    cls.default_connection = default_connection
    cls.rule = rule
    cls.type = type

    return cls
