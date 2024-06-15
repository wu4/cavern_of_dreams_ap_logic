from collections.abc import Generator, Iterable
from dataclasses import dataclass
from typing import Literal, TypeAlias
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

from ..logic.logic import ChainableLogic, Logic
from ..logic.logic import Any
from ..logic.logic import All
from ..logic.carrying import Carrying
from ..logic.has import CarryingItem
from ..logic.comment import Comment

# -1 = no requirements
# None | CarryingItem = requires carrying
CarryingTestResult: TypeAlias = CarryingItem | None | Literal[-1]

class CarryingTestParser:
  stack: list[Logic]

  def __init__(self):
    super().__init__()
    self.stack = []

  def parse(self, logic: Logic) -> dict[CarryingTestResult, Logic]:
    if isinstance(logic, Carrying):
      return {logic.carryable: logic}
    elif isinstance(logic, Comment):
      return self.parse(logic.logic)
    elif isinstance(logic, All):
      ret: dict[CarryingTestResult, Logic] = {}
      for logic in logic.operands:
        if not isinstance(logic, ChainableLogic)
      return ret

def carrying_test(logic: Logic) -> set[CarryingTestResult]:
  if isinstance(logic, Carrying):
    return {logic.carryable}
  elif isinstance(logic, Comment):
    return carrying_test(logic.logic)
  elif isinstance(logic, ChainableLogic):
    types: set[CarryingTestResult] = set()
    for u in map(carrying_test, logic.operands):
      types.update(u)
    return types
  else:
    return {-1}

def split_operands(logic: Logic) -> dict[CarryingTestResult, list[Logic]]:
  if isinstance(logic, Comment):
    return split_operands(logic.logic)

  test = carrying_test(logic)

  if len(test) == 1 or not isinstance(logic, ChainableLogic):
    return {item: [logic] for item in test}

  splits: dict[CarryingTestResult, list[Logic]] = {}

  if isinstance(logic, Any):
    for op in logic.operands:
      op_test = carrying_test(op)
      c = split_operands(op)
      for item in test & op_test:
        splits.setdefault(item, []).extend(c[item])
  else:
    for op in logic.operands:
      c = split_operands(op)
      for k, v in c.items():
        splits.setdefault(k, []).extend(v)

  return splits

def into_server_code(logic: Logic):
  requires_carrying = split_operands(logic)
  print("===========")
  print(logic)
  print(carrying_test(logic))
  print("===========")
  for k, v in requires_carrying.items():
    print(k)
    print(list(map(str, v)))

  # print(list(map(str, others)))

def region_name(region: type[Region]) -> str:
  module = region.__module__.split(".")
  return ".".join([*module[2:], region.__name__])

def serialize_region_connections(region: type[Region], assigned_regions: dict[type[Region], str]) -> list[str]:
  connecting_region_names: list[str] = []
  connecting_region_rules: dict[str, str] = {}

  for connecting_region, logic in region.region_connections.items():
    connecting_region_name = region_name(connecting_region)
    connecting_region_names.append(connecting_region_name)
    if logic is not None:
      into_server_code(logic)
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
    str_ret.append(f"r{region_id}=R({region_name(region).__repr__()},p,mw)")
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
