from collections.abc import Generator, Iterable
from ..logic import Region, Entrance

from ..levels.CAVE import SunCavern

class ConnectionParser:
  def parse(self, region: type[Region]):
    if region in self.seen_regions: return
    self.seen_regions.append(region)

    for inner_region in region.region_connections.keys():
      self.parse(inner_region)

    for entrance in region.entrances:
      if entrance in self.seen_entrances: continue
      self.seen_entrances.append(entrance)
      self.parse(entrance.default_connection.containing_region)

  def __init__(self) -> None:
    super().__init__()
    self.seen_regions: list[type[Region]] = []
    self.seen_entrances: list[type[Entrance]] = []

def region_name(region: type[Region]) -> str:
  module = region.__module__.split(".")
  return ".".join([*module[2:], region.__name__])

def serialize_region_connections(region: type[Region], assigned_regions: dict[type[Region], str]) -> list[str]:
  connecting_region_names: list[str] = []
  connecting_region_rules: dict[str, str] = {}

  for connecting_region, logic in region.region_connections.items():
    connecting_region_name = region_name(connecting_region)
    connecting_region_names.append(connecting_region_name)
    connecting_region_rules[connecting_region_name] = "None" if logic is None else logic.into_server_code()

  accum: list[str] = []
  for connecting_region, rule in region.region_connections.items():
    accum.append(f"# {region_name(region)} -> {region_name(connecting_region)}")
    accum.append(f"{assigned_regions[region]}.connect({assigned_regions[connecting_region]},{'None' if rule is None else 'lambda s:'+rule.into_server_code()})")

  return accum

def assign_regions(regions: Iterable[type[Region]]) -> tuple[list[str], dict[type[Region], str]]:
  region_id: int = 0
  str_ret: list[str] = []
  regs_ret: dict[type[Region], str] = {}
  for region in regions:
    str_ret.append(f"r{region_id}=R(\"{region_name(region)}\",p,mw)")
    regs_ret[region] = f"r{region_id}"
    region_id += 1

  return str_ret, regs_ret

def indent(lines: Iterable[str], indent_level: int) -> Generator[str, None, None]:
  for line in lines:
    yield ("    " * indent_level) + line

def generate():
  parser = ConnectionParser()
  parser.parse(SunCavern.Main)
  accum: list[str] = []
  accum.append("from BaseClasses import Entrance as E")
  accum.append("from ..regions import CavernOfDreamsRegion as R")

  # entrances require regions to exist
  # there are plenty of circular dependencies here, so a simple tsort wouldnt
  #  be enough

  accum.append("def create_regions(world):")
  accum += indent([
    "p=world.player",
    "o=world.options",
    "mw=world.multiworld",
  ], 1)

  regions_accum, assigned_regions = assign_regions(parser.seen_regions)
  accum += indent(regions_accum, 1)

  for region in parser.seen_regions:
    accum += indent(serialize_region_connections(region, assigned_regions), 1)

  with open("ap_generated/regions.py", "w") as out_py:
    _ = out_py.write("\n".join(accum))
