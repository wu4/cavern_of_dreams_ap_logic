from abc import abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, TypeAlias, override

from logic.carrying import Carrying
from .. import all_locations
from .connection_parser import all_regions, all_entrances
from ..logic_parsing.options import get_required_options
from ..logic_parsing.helpers import nested_list_to_logic

if TYPE_CHECKING:
  from ..logic.logic import MaybeLogic
  from ..logic_parsing.carryables import CarryableKey

from ..logic import Region, Entrance

def name_regions(regs: Iterable[Region]) -> dict[Region, str]:
  return dict(
    (region, f"r{region_id}")
    for region_id, region in enumerate(regs)
  )

region_names = name_regions(all_regions)

class Builder:
  lines: list[str]
  indent: int

  def __init__(self):
    super().__init__()
    self.lines = []
    self.indent = 0

  def add_line(self, line: str):
    self.lines.append(("  " * self.indent) + line)

  @abstractmethod
  def run(self): ...

  @classmethod
  def build(cls) -> str:
    a = cls()
    a.run()
    return "\n".join(a.lines)

class ItemsBuilder(Builder):
  @override
  def run(self):
    self.add_items()
    self.add_line("from BaseClasses import Entrance as E")
    self.add_line("from ..regions import CavernOfDreamsRegion as R")
    self.add_line("from ..entrance_rando import randomize_entrances")
    self.add_line("def create_regions(world):")
    self.indent += 1
    self.add_line("p=world.player")
    self.add_line("o=world.options")
    self.add_line("mw=world.multiworld")
    self.add_line("if o.entrance_rando:")
    self.indent += 1
    self.indent -= 1
    self.add_line("else:")
    self.indent += 1
    self.indent -= 1
    self.add_line(f"M=R('Menu',p,mw)")
    self.add_line("if o.start_location == 0:")
    self.indent += 1

  def add_items(self):
    for item_name in all_locations.all_items():
      self.add_line(repr(item_name) + ",")

RegionAndRule: TypeAlias = tuple[Region, "MaybeLogic"]

class RegionsBuilder(Builder):
  @override
  def run(self):
    from ..levels.CAVE import SunCavern
    from ..levels.GALLERY import Foyer
    self.add_line("from ..regions import CavernOfDreamsRegion as R, CavernOfDreamsEntrance as E, CavernOfDreamsLocation as L, CavernOfDreamsCarryableRegion as CR")
    # self.add_line("from ..items import CavernOfDreamsEvent as EV")
    self.add_line("from ..entrance_rando import randomize_entrances")
    self.add_line("from .data import item_group_sets")
    self.add_line("all_eggs=item_group_sets['Egg']")
    # self.add_line("from ..item_rules import is_shroom")
    self.define_entrances()
    self.add_line("def create_regions(w):")
    self.indent += 1
    self.add_line("p=w.player")
    self.add_line("o=w.options")
    self.add_line("mw=w.multiworld")
    self.assign_regions()
    self.connect_regions()
    self.define_locations()
    # self.add_line("if o.entrance_rando:")
    # self.indent += 1
    # self.entrance_rando()
    # self.indent -= 1
    # self.add_line("else:")
    # self.indent += 1
    self.no_entrance_rando()
    # self.indent -= 1
    self.add_line(f"M=R('Menu',p,mw)")
    # self.add_line("if o.start_location == 0:")
    # self.indent += 1
    self.connect_str(
      "Menu", "M",
      SunCavern.Main.name, region_names[SunCavern.Main],
      None
    )
    self.add_line("mw.regions.append(M)")
    self.add_line(f"e=w.create_event('Victory')")
    self.add_line(f"l=L(p,'VictoryLocation',False,{region_names[Foyer.Endgame]})")
    self.add_line(f"l.place_locked_item(e)")
    self.add_line(f"{region_names[Foyer.Endgame]}.locations.append(l)")

  def connect_short(
    self, start_id: str, to_id: str, rule: "MaybeLogic",
    name: str | None = None
  ):
    if name is None:
      name_str = f"{start_id}.name+'->'+{to_id}.name"
    else:
      name_str = repr(name)
    self.add_line(f"e=E(p,{name_str},{start_id})")
    self.add_line(f"{start_id}.exits.append(e)")
    self.add_line(f"e.connect({to_id})")

    self.define_rules(rule, "e")

  def connect_str(
    self,
    start_name: str, start_id: str,
    to_name: str, to_id: str,
    rule: "MaybeLogic",
    name: str | None = None
  ):
    self.add_line(f"# {start_name} -> {to_name}")
    self.connect_short(start_id, to_id, rule, name)

  def define_rules(self, rule: "MaybeLogic", var_name: str):
    if rule is None:
      # self.add_line(f"{var_name}.can_reach={var_name}.simple_can_reach")
      return

    from ..logic_parsing.carryables import distribute_carryable_logic
    from ..logic_parsing.helpers import simplify
    from ..logic.logic import Not

    distributed = distribute_carryable_logic(rule)
    def sort_by_branch_count(k: "CarryableKey"):
      return sum(map(len, distributed[k]))

    carryable_keys_by_branch_count = sorted(list(distributed.keys()), key=sort_by_branch_count)

    if "dont-care" in carryable_keys_by_branch_count:
      logic = simplify(distributed["dont-care"])
      self.add_line(f"{var_name}.dont_care_access_rule=lambda s:{logic.into_server_code()}")
    else:
      self.add_line(f"{var_name}.dont_care_access_rule=lambda s:False")

    self.add_line(f"{var_name}.not_carryable_access_rules="+'{')
    self.indent += 1
    for key in carryable_keys_by_branch_count:
      if not isinstance(key, Not): continue
      assert isinstance(key.logic, Carrying)

      nested_list = distributed[key]
      if nested_list == []:
        logic_str = "lambda s:True"
      else:
        logic = simplify(nested_list)
        logic_str = f"lambda s:{logic.into_server_code()}"
      self.add_line(f"{repr(key.logic.carryable)}:{logic_str},")
    self.indent -= 1
    self.add_line("}")

    self.add_line(f"{var_name}.carryable_access_rules="+'{')
    self.indent += 1
    for key in carryable_keys_by_branch_count:
      if key == "default": continue
      if isinstance(key, Not): continue

      nested_list = distributed[key]
      if nested_list == []:
        logic_str = "lambda s:True"
      else:
        logic = simplify(nested_list)
        logic_str = f"lambda s:{logic.into_server_code()}"
      self.add_line(f"{repr(key.carryable)}:{logic_str},")
    self.indent -= 1
    self.add_line("}")

  def define_rule(self, rule: "MaybeLogic"):
    if rule is None: return False
    self.add_line("def rule(s):")
    self.indent += 1
    from ..logic_parsing.carryables import distribute_carryable_logic
    from ..logic_parsing.helpers import simplify
    from ..logic.logic import Not
    distributed = distribute_carryable_logic(rule)
    def sort_key(k):
      return sum(map(len, distributed[k]))
    distributed_keys = list(distributed.keys())

    # anything that does not care about carryables
    if "default" in distributed_keys:
      logic = simplify(distributed["default"])
      self.add_line(f"if {logic.into_server_code()}: return True")

    if len(list(filter("default".__ne__, distributed_keys))) > 0:
      self.add_line("carryable=s._cavernofdreams_carrying[p]")

    # process Nots before the rest
    # NOTE: Nots should not early-out if they return false
    for key in sorted(filter(lambda k: isinstance(k, Not), distributed_keys), key=sort_key):
      self.add_line(f"if carryable!={repr(key.logic.carryable)}:")
      self.indent += 1
      nested_list = distributed[key]
      if nested_list == []:
        self.add_line("return True")
      else:
        logic = simplify(nested_list)
        self.add_line(f"if {logic.into_server_code()}: return True")
      self.indent -= 1

    is_first = True
    for key in sorted(filter(lambda k: k != "default" and not isinstance(k, Not), distributed_keys), key=sort_key):
      if key.carryable is None:
        self.add_line(f"{'' if is_first else 'el'}if carryable is None:")
      else:
        self.add_line(f"{'' if is_first else 'el'}if carryable=={repr(key.carryable)}:")
      self.indent += 1
      nested_list = distributed[key]
      if nested_list == []:
        self.add_line("return True")
      else:
        logic = simplify(nested_list)
        self.add_line(f"return {logic.into_server_code()}")
      self.indent -= 1
      is_first = False

    self.add_line("return False")
    self.indent -= 1
    return True

  def connect(self, start: Region, to: Region, rule: "MaybeLogic", name: str | None = None):
    self.connect_str(
      start.name, region_names[start],
      to.name, region_names[to],
      rule,
      name
    )

  def define_locations(self):
    from ..logic.objects import CarryableLocation, InternalEvent

    locations: dict[str, RegionAndRule] = {}
    carryable_locations: dict[type[CarryableLocation], RegionAndRule] = {}
    internal_events: dict[type[InternalEvent], RegionAndRule] = {}

    for region in all_regions:
      for location, rule in region.locations.items():
        if isinstance(location, str):
          locations[location] = (region, rule)
        elif issubclass(location, CarryableLocation):
          carryable_locations[location] = (region, rule)
        else:
          internal_events[location] = (region, rule)

    self.add_line("shroomsanity=o.shroomsanity.value==1")
    for category_name, locations_list in all_locations.locations_by_category():
      # self.add_line(f"if o.{category}_rando:")
      # self.indent += 1
      for location in locations_list:
        region, rule = locations[location]
        self.add_line(f"l=L(p,{repr(location)},True,{region_names[region]})")
        # if category_name == "shroom":
        #   self.add_line("if not shroomsanity:l.item_rule=is_shroom")
        self.define_rules(rule, "l")
        self.add_line(f"{region_names[region]}.locations.append(l)")

    for location, (region, rule) in internal_events.items():
      rule_indent = 0
      if rule is not None:
        required_options = get_required_options(rule)
        if len(required_options) > 0:
          logic = nested_list_to_logic(required_options)
          self.add_line(f"if {logic.into_server_code()}:")
          rule_indent = 1

      self.indent += rule_indent
      self.add_line(f"l=L(p,{repr(str(location))},False,{region_names[region]})")
      self.define_rules(rule, "l")

      self.add_line(f"e=w.create_event({repr(str(location))})")
      self.add_line(f"l.place_locked_item(e)")

      self.add_line(f"{region_names[region]}.locations.append(l)")
      self.indent -= rule_indent

    for location, (region, rule) in carryable_locations.items():
      name = repr(str(location))
      self.add_line(f"r=CR({name},p,mw,{repr(location.carryable)})")
      # self.add_line(f"l=L(p,{name},None,r)")
      # if rule is not None:
      #   self.add_line(f"l.access_rule={into_ap_rule(rule)}")

      # self.add_line(f"e=w.create_event({name})")
      # self.add_line(f"l.place_locked_item(e)")

      # self.add_line(f"r.locations.append(l)")
      self.add_line(f"{region_names[region]}.connect(r)")
      self.add_line(f"r.connect({region_names[region]})")
      self.add_line(f"mw.regions.append(r)")

    # self.indent -= 1

  def assign_regions(self):
    for region in all_regions:
      name = region_names[region]
      self.add_line(f"{name}=R({repr(region.name)},p,mw)")
      self.add_line(f"mw.regions.append({name})")

  def connect_regions(self):
    for region in all_regions:
      for connecting_region, rule in region.region_connections.items():
        self.connect(region, connecting_region, rule)

  def define_entrance_list(self, list_name: str, entrances: list[tuple[type[Entrance], type[Entrance]]]):
    self.add_line(f"{list_name}:list[tuple[str,str]]=[")
    self.indent += 1
    for entry, exit in entrances:
      self.add_line(repr((entry.name(), exit.name())) + ",")
    self.indent -= 1
    self.add_line("]")

  def entrance_rando(self):
    self.define_entrance_map()
    self.define_entrance_rules()
    self.randomize_entrances()

  def randomize_entrances(self):
    self.add_line("rando_bilinear=randomize_entrances(bilinear)")
    self.add_line("rando_one_way=randomize_entrances(one_way)")
    self.add_line("for start,to in rando_bilinear:")
    self.indent += 1
    self.add_line(f"entrance_map[start].connect(entrance_map[to],start,entrance_rules.get(start,None))")
    self.add_line(f"entrance_map[to].connect(entrance_map[start],to,entrance_rules.get(to,None))")
    self.indent -= 1
    self.add_line("for start,to in rando_one_way:")
    self.indent += 1
    self.add_line(f"entrance_map[start].connect(entrance_map[to],start,entrance_rules.get(start,None))")
    self.indent -= 1

  def define_entrance_rules(self):
    self.add_line("entrance_rules={}")
    # self.indent += 1
    for entrance in all_entrances:
      rule_var = 'rule' if self.define_rule(entrance.rule) else 'None'
      self.add_line(f"entrance_rules[{repr(entrance.name())}]={rule_var}")
    # self.indent -= 1
    # self.add_line("}")

  def define_entrance_map(self):
    self.add_line("entrance_map:dict[str,R]={")
    self.indent += 1
    for entrance in all_entrances:
      self.add_line(f"{repr(entrance.name())}:{region_names[entrance.containing_region]},")
    self.indent -= 1
    self.add_line("}")

  def define_entrances(self):
    bilinear_connections: set[tuple[type[Entrance], type[Entrance]]] = set()
    one_way_connections: set[tuple[type[Entrance], type[Entrance]]] = set()

    for entrance in all_entrances:
      if entrance.warp_path is None:
        if (entrance.default_connection, entrance) in one_way_connections: continue
        one_way_connections.add((entrance.default_connection, entrance))
      elif entrance.dest_path is None:
        if (entrance, entrance.default_connection) in one_way_connections: continue
        one_way_connections.add((entrance, entrance.default_connection))
      else:
        if (entrance.default_connection, entrance) in one_way_connections: continue
        bilinear_connections.add((entrance, entrance.default_connection))

    self.define_entrance_list("bilinear", list(bilinear_connections))
    self.define_entrance_list("one_way", list(one_way_connections))

  def no_entrance_rando(self):
    for entrance in all_entrances:
      if entrance.warp_path is not None:
        self.connect(entrance.containing_region, entrance.default_connection.containing_region, entrance.rule, entrance.name())

def generate():
  with open("ap_generated/regions.py", "w") as out_py:
    _ = out_py.write(RegionsBuilder.build())
