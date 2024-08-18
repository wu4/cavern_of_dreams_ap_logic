from collections.abc import Iterable
from typing import TYPE_CHECKING, TypeAlias, override

from .builder import Builder

from .. import all_locations
from .connection_parser import all_regions
from ..logic_parsing.options import get_required_options
from ..logic_parsing.helpers import nested_list_to_logic

if TYPE_CHECKING:
  from ..logic.logic import MaybeLogic

from ..logic import Region

def name_regions(regs: Iterable[Region]) -> dict[Region, str]:
  return dict(
    (region, f"r{region_id}")
    for region_id, region in enumerate(regs)
  )

region_names = name_regions(all_regions)

RegionAndRule: TypeAlias = tuple[Region, "MaybeLogic"]

class ConditionalIndent:
  builder: Builder
  def __init__(self, builder: Builder, block_starter: str | None) -> None:
    self.builder = builder
    self.block_starter = block_starter

  def __enter__(self):
    if self.block_starter is not None:
      self.builder.add_line(self.block_starter)
      self.builder.indent += 1

  def __exit__(self, exc_type, exc_value, traceback):
    if self.block_starter is not None:
      self.builder.indent -= 1

class RegionsBuilder(Builder):
  @override
  def run(self):
    from ..levels.GALLERY import Foyer
    self.add_line("from ..regions import CavernOfDreamsRegion as R, CavernOfDreamsEntrance as E, CavernOfDreamsLocation as L")
    self.add_line("from ..generated_helpers import construct_rule")
    self.add_line("from ..item_rules import no_carryables, no_carryables_or_eggs")
    self.add_line("from ..custom_start_location import get_starting_region_name")
    self.add_line("def create_regions(w):")
    self.indent += 1
    self.add_line("p=w.player")
    self.add_line("o=w.options")
    self.add_line("mw=w.multiworld")
    self.assign_regions()
    self.connect_regions()
    self.define_locations()
    # self.add_line("if not o.entrance_rando:")
    # self.indent += 1
    # self.no_entrance_rando()
    # self.indent -= 1
    self.add_line(f"M=R('Menu',p,mw)")
    # self.add_line("if o.start_location == 0:")
    # self.indent += 1
    self.connect_short(
      "M", "mw.get_region(get_starting_region_name(o),p)",
      None,
      "Menu"
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
          with ConditionalIndent(self,
            "if o.shroomsanity:" if category_name == "shroom" else None
          ):
            self.add_line("cl.append(l)")

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
      with ConditionalIndent(self,
        "if o.carry_through_doors:" if region.unreachable_if_no_carry_through_doors else None
      ):
        def maybe_get_option_conditions():
          if rule is None: return None
          required_options = get_required_options(rule)

          if len(required_options) == 0: return None

          logic = nested_list_to_logic(required_options)
          return f"if {logic.into_server_code()}:"

        with ConditionalIndent(self, maybe_get_option_conditions()):
          self.add_line(f"l=L(p,{repr(str(location))},False,{region_names[region]})")
          self.define_rules(rule, "l")

          self.add_line(f"e=w.create_event({repr(str(location))})")
          self.add_line(f"l.place_locked_item(e)")
          self.add_line(f"l.item_rule=no_carryables")

          self.add_line(f"{region_names[region]}.locations.append(l)")

  def assign_regions(self):
    for region in all_regions:
      name = region_names[region]
      with ConditionalIndent(self,
        "if o.carry_through_doors:" if region.unreachable_if_no_carry_through_doors else None
      ):
        self.add_line(f"{name}=R({repr(region.name)},p,mw)")
        self.add_line(f"mw.regions.append({name})")

  def connect_regions(self):
    for region in all_regions:
      if len(region.region_connections) == 0: continue

      with ConditionalIndent(self,
        "if o.carry_through_doors:" if region.unreachable_if_no_carry_through_doors else None
      ):
        for connecting_region, rule in region.region_connections.items():
          with ConditionalIndent(self,
            "if o.carry_through_doors:" if connecting_region.unreachable_if_no_carry_through_doors else None
          ):
            self.connect(region, connecting_region, rule)

  # def no_entrance_rando(self):
  #   for entrance in all_entrances:
  #     if entrance.warp_path is not None:
  #       self.connect(entrance.containing_region, entrance.default_connection.containing_region, entrance.rule, entrance.name())

def generate(first_line: str):
  with open("ap_generated/regions.py", "w") as out_py:
    _ = out_py.write(f"{first_line}\n")
    _ = out_py.write(RegionsBuilder.build())
