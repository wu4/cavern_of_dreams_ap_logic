from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from ..logic import Region, Entrance

class ConnectionParser:
  def __init__(self) -> None:
    super().__init__()
    self.seen_regions: list["Region"] = []
    self.seen_entrances: list[type["Entrance"]] = []

  def parse(self, region: "Region"):
    if region in self.seen_regions: return
    region.lazy_load()
    self.seen_regions.append(region)

    for inner_region in region.region_connections.keys():
      self.parse(inner_region)

    for entrance in region.entrances:
      if entrance in self.seen_entrances: continue
      self.seen_entrances.append(entrance)
      self.parse(entrance.default_connection.containing_region)

cached: bool = False
seen_regions: list["Region"] = []
seen_entrances: list[type["Entrance"]] = []

def parse():
  global cached, seen_regions, seen_entrances
  if not cached:
    parser = ConnectionParser()
    from ..levels.CAVE import SunCavern
    parser.parse(SunCavern.Main)
    seen_regions = parser.seen_regions
    seen_entrances = parser.seen_entrances
    cached = True
  return seen_regions, seen_entrances
