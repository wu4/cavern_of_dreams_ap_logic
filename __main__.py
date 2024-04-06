from .logic import Region, Entrance

from .levels.CAVE import SunCavern

class ConnectionParser:
  def parse(self, region: type[Region]):
    if region in self.seen_regions: return
    print(region.__module__ + '.' + region.__name__)
    for location, logic in region.locations.items():
      print(location, logic)
    self.seen_regions.add(region)

    for inner_region in region.region_connections:
      self.parse(inner_region)
      
    for entrance in region.entrances:
      self.parse(entrance.to.containing_region)

  def __init__(self) -> None:
    self.seen_regions: set[type[Region]] = set()
    self.seen_entrances: set[type[Entrance]] = set()

ConnectionParser().parse(SunCavern.Main)