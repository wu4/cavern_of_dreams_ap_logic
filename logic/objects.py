from __future__ import annotations
from . import MaybeLogic as _MaybeLogic
from ..generated import AnyLocation

from typing import TypeAlias
from dataclasses import dataclass

class InternalEvent:
  pass

class CarryableLocation:
  pass

class AppleTree(CarryableLocation):
  pass

class JesterBoots(CarryableLocation):
  pass

LocationType: TypeAlias = AnyLocation | type[InternalEvent] | type[CarryableLocation]

class Region:
  _is_defined: bool = False

  @classmethod
  def define(
    cls,
    region_connections: dict[type[Region], _MaybeLogic] = {},
    entrances: list[type[Entrance]] = [],
    locations: dict[LocationType, _MaybeLogic] = {}
  ) -> type[Region]:
    assert not cls._is_defined, f"Tried to redefine {cls.__name__}"
    cls._is_defined = True

    cls.region_connections = region_connections
    cls.locations = locations
    cls.entrances = entrances
    for entrance in entrances:
      entrance.set_containing_region(cls)
    
    return cls

class Entrance:
  _is_defined: bool = False
  
  @classmethod
  def set_containing_region(cls, region: type[Region]):
    cls.containing_region = region

  @classmethod
  def define(cls, to: type[Entrance], rule: _MaybeLogic = None) -> type[Entrance]:
    assert not cls._is_defined, f"Tried to redefine {cls.__name__}"
    cls._is_defined = True

    cls.to = to
    cls.rule = rule

    return cls