from __future__ import annotations
from . import MaybeLogic as _MaybeLogic
from ..generated import AnyLocation

from typing import Self, TypeAlias

class InternalEvent:
  def __init__(self, pretty_name: str):
    super().__init__()
    self.pretty_name = pretty_name

class CarryableLocation:
  def __init__(self, pretty_name: str):
    super().__init__()
    self.pretty_name = pretty_name

class AppleTreeLocation(CarryableLocation):
  pass

class JesterBootsLocation(CarryableLocation):
  pass

LocationType: TypeAlias = AnyLocation | InternalEvent | CarryableLocation

class Region:
  def __init__(
    self,
    pretty_name: str,
  ):
    super().__init__()
    self._is_defined = False
    self.pretty_name = pretty_name

    self.region_connections = {}
    self.entrances = []
    self.locations = {}

  def define(
    self,
    region_connections: dict[Region, _MaybeLogic] | None = None,
    entrances: list[Entrance] | None = None,
    locations: dict[LocationType, _MaybeLogic] | None = None
  ) -> Self:
    assert not self._is_defined, f"Tried to redefine {self.pretty_name}"
    self._is_defined = True

    if region_connections is not None:
      self.region_connections = region_connections
    if entrances is not None:
      self.entrances = entrances
    if locations is not None:
      self.locations = locations

    for entrance in self.entrances:
      entrance.set_containing_region(self)

    return self

class Entrance:
  def set_containing_region(self, region: Region):
    self.containing_region = region

  def __init__(
    self,
    pretty_name: str
  ):
    super().__init__()
    self.to: Entrance
    self.rule: _MaybeLogic
    self.containing_region: Region

    self._is_defined = False
    self.pretty_name = pretty_name

  def define(self, to: Entrance, rule: _MaybeLogic = None) -> Self:
    assert not self._is_defined, f"Tried to redefine {self.pretty_name}"
    self._is_defined = True

    self.to = to
    self.rule = rule

    return self
