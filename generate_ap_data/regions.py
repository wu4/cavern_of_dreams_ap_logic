from abc import abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, TypeAlias, override

from ..logic.carrying import Carrying
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
    self.add_line("from ..regions import CavernOfDreamsRegion as R, CavernOfDreamsEntrance as E, CavernOfDreamsLocation as L")
    # self.add_line("from ..items import CavernOfDreamsEvent as EV")
    self.add_line("from ..entrance_rando import randomize_entrances")
    self.add_line("from .data import item_group_sets")
    self.add_line("from ..item_rules import no_carryables, no_carryables_or_eggs")
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
    self.add_line(f"l.access_rule = lambda s:True")
    self.add_line(f"{region_names[Foyer.Endgame]}.locations.append(l)")
    self.add_line("return cl")

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

  def define_dict(self, var_name: str, dictionary: dict[str, str]):
    self.add_line(f"{var_name}="+'{')
    self.indent += 1
    for k, v in dictionary.items():
      self.add_line(f"{k}:{v},")
    self.indent -= 1
    self.add_line("}")

  def define_rules(self, rule: "MaybeLogic", var_name: str):
    if rule is None:
      self.add_line(f"{var_name}.dont_care_access_rule=lambda s:True")
      return

    from ..logic_parsing.carryables import distribute_carryable_logic
    from ..logic_parsing.helpers import simplify
    from ..logic.logic import Not

    distributed = distribute_carryable_logic(rule)
    def sort_by_branch_size(k: "CarryableKey"):
      return sum(map(len, distributed[k]))

    cases_by_branch_size = sorted(list(distributed.keys()), key=sort_by_branch_size)

    def get_simplified_logic(case: "CarryableKey"):
      logic = distributed[case]
      return "True" if logic == [] else simplify(logic).into_server_code()

    inverse_rules: dict[str, str] = {}
    rules: dict[str, str] = {}

    for case in cases_by_branch_size:
      # handle this below
      if case == "dont-care": continue

      case_rule = f"lambda s:{get_simplified_logic(case)}"
      if isinstance(case, Not):
        assert isinstance(case.logic, Carrying)
        inverse_rules[repr(case.logic.carryable)] = case_rule
      else:
        rules[repr(case.carryable)] = case_rule

    if "dont-care" in cases_by_branch_size:
      dont_care_rule = f"lambda s:{get_simplified_logic('dont-care')}"
      self.add_line(f"{var_name}.dont_care_access_rule={dont_care_rule}")

    self.define_dict(f"{var_name}.inverse_carryable_access_rules", inverse_rules)
    self.define_dict(f"{var_name}.carryable_access_rules", rules)


  def connect(self, start: Region, to: Region, rule: "MaybeLogic", name: str | None = None):
    self.connect_str(
      start.name, region_names[start],
      to.name, region_names[to],
      rule,
      name
    )

  def define_locations(self):
    from ..logic.objects import InternalEvent

    locations: dict[str, RegionAndRule] = {}
    # carryable_locations: dict[type[CarryableLocation], RegionAndRule] = {}
    internal_events: dict[type[InternalEvent], RegionAndRule] = {}

    for region in all_regions:
      for location, rule in region.locations.items():
        if isinstance(location, str):
          locations[location] = (region, rule)
        # elif issubclass(location, CarryableLocation):
        #   carryable_locations[location] = (region, rule)
        else:
          internal_events[location] = (region, rule)

    # self.add_line("shroomsanity=o.shroomsanity.value==1")
    self.add_line("cl=[]")
    for category_name, locations_list in all_locations.locations_by_category():
      # self.add_line(f"if o.{category}_rando:")
      # self.indent += 1
      category_no_carryables = category_name in {
        "event", "gratitude", "ability"
      }

      for location in locations_list:
        region, rule = locations[location]

        self.add_line(f"l=L(p,{repr(location)},True,{region_names[region]})")

        location_no_carryables = category_no_carryables or (location in all_locations.carryables_blacklist)
        if location_no_carryables:
          if location == "Sun Cavern - Sage's Blessing 5":
            self.add_line("l.item_rule=no_carryables_or_eggs")
          else:
            self.add_line("l.item_rule=no_carryables")
        else:
          cl_indent = 0
          if category_name == "shroom":
            self.add_line("if o.shroomsanity:")
            cl_indent = 1

          self.indent += cl_indent
          self.add_line("cl.append(l)")
          self.indent -= cl_indent

        # if category_name == "shroom":
        #   self.add_line("if not shroomsanity:l.item_rule=is_shroom")
        self.define_rules(rule, "l")
        self.add_line(f"{region_names[region]}.locations.append(l)")

    # for location, (region, rule) in carryable_locations.items():
    #   name = repr(location.location_name)
    #   self.add_line(f"l=L(p,{name},True,{region_names[region]})")
    #   self.define_rules(rule, "l")
    #   self.add_line(f"{region_names[region]}.locations.append(l)")

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
      self.add_line(f"l.item_rule=no_carryables")

      self.add_line(f"{region_names[region]}.locations.append(l)")
      self.indent -= rule_indent

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
    # for entrance in all_entrances:
    #   rule_var = 'rule' if self.define_rule(entrance.rule) else 'None'
    #   self.add_line(f"entrance_rules[{repr(entrance.name())}]={rule_var}")
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
