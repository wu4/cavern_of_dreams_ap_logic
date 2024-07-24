from types import ModuleType
from typing import TYPE_CHECKING
from inspect import getmodule

from ..logic import Region
if TYPE_CHECKING:
  from ..logic import Entrance

class ConnectionParser:
  loaded_modules: set[ModuleType] = set()

  def __init__(self) -> None:
    super().__init__()
    self.seen_regions: list["Region"] = []
    self.seen_entrances: list[type["Entrance"]] = []

  def lazy_load_connecting_regions(self, region: "Region"):
    for entrance in region.entrances:
      mod = getmodule(entrance.default_connection)
      assert mod is not None
      if mod not in self.loaded_modules:
        self.loaded_modules.add(mod)
        for k, v in mod.__dict__.items(): # type: ignore [reportAny]
          if isinstance(v, Region):
            v.lazy_load()

  def parse(self, region: "Region"):
    if region in self.seen_regions: return
    region.lazy_load()

    self.lazy_load_connecting_regions(region)

    self.seen_regions.append(region)

    for inner_region in region.region_connections.keys():
      self.parse(inner_region)

    for entrance in region.entrances:
      if entrance in self.seen_entrances: continue
      self.seen_entrances.append(entrance)
      self.parse(entrance.default_connection.containing_region)

_is_cached: bool = False
_regions: list["Region"] = []
_entrances: list[type["Entrance"]] = []

all_regions: list["Region"]
all_entrances: list[type["Entrance"]]

def __getattr__(name: str):
  global _is_cached, _regions, _entrances
  if name in {"all_regions", "all_entrances"}:
    if not _is_cached:
      parser = ConnectionParser()
      from ..levels.CAVE import SunCavern
      parser.parse(SunCavern.Main)
      _regions = parser.seen_regions
      _entrances = parser.seen_entrances
    if name == "all_regions":
      return _regions
    else:
      return _entrances
