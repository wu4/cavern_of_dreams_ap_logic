from .logic import Region, Entrance

from .levels.CAVE import SunCavern

class ConnectionParser:
  def parse(self, region: type[Region]):
    if region in self.seen_regions: return
    print(region.__module__ + '.' + region.__name__)
    for location, logic in region.locations.items():
      if logic is not None:
        print(location, logic.into_server_code())
    self.seen_regions.add(region)

    for inner_region, logic in region.region_connections.items():
      if logic is not None:
        print(inner_region.__name__, logic.into_server_code())
      self.parse(inner_region)

    for entrance in region.entrances:
      self.parse(entrance.default_connection.containing_region)

  def __init__(self) -> None:
    super().__init__()
    self.seen_regions: set[type[Region]] = set()
    self.seen_entrances: set[type[Entrance]] = set()

ConnectionParser().parse(SunCavern.Main)
