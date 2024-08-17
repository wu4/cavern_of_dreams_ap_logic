from typing import override

from ..logic import carrying
from ..logic.objects import Entrance
from .builder import Builder
from .connection_parser import all_entrances

def entrance_name_and_path(entrance: type[Entrance]) -> str:
  return repr(f"{entrance.containing_region.name}.{entrance.__name__}")

class EntranceRandoBuilder(Builder):
  @override
  def run(self):
    self.add_line("from ..regions import CavernOfDreamsRegion as R, CavernOfDreamsEntrance as E, CavernOfDreamsLocation as L")
    self.add_line("from ..generated_helpers import construct_rule")
    self.define_entrance_rando_connections()
    self.define_region_parents()
    self.define_underwater_destinations()
    self.add_line("def create_entrances(w):")
    self.indent += 1
    self.add_line("p=w.player")
    self.add_line("o=w.options")
    self.add_line("mw=w.multiworld")
    self.define_entrances()
    self.indent -= 1

  def define_region_parents(self):
    self.define_dict("parent_regions:dict[str,str]",{
      entrance_name_and_path(entrance): repr(entrance.containing_region.name)
      for entrance in all_entrances
    })

  def define_entrance_list(self, list_name: str, entrances: list[tuple[type[Entrance], type[Entrance]]]):
    self.add_line(f"{list_name}:list[tuple[str,str]]=[")
    self.indent += 1
    for entry, exit in entrances:
      self.add_line(f"({entrance_name_and_path(entry)},{entrance_name_and_path(exit)}),")
    self.indent -= 1
    self.add_line("]")

  def define_entrance_rando_connections(self):
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
        if (entrance.default_connection, entrance) in bilinear_connections: continue
        bilinear_connections.add((entrance, entrance.default_connection))

    self.define_entrance_list("bilinear", list(bilinear_connections))
    self.define_entrance_list("one_way", list(one_way_connections))

  def define_underwater_destinations(self):
    self.add_line("underwater_destinations:set[str]={")
    self.indent += 1
    for entrance in all_entrances:
      if not entrance.is_dest_underwater: continue
      self.add_line(f"{entrance_name_and_path(entrance)},")
    self.indent -= 1
    self.add_line("}")

  def define_entrances(self):
    self.add_line("entrances:dict[str,tuple[E|None,bool]]={}")
    for entrance in all_entrances:
      if entrance.warp_path is None:
        self.add_line(f"entrances[{entrance_name_and_path(entrance)}]=(None,{repr(entrance.is_dest_underwater)})")
      self.add_line(f"e=E(p,{entrance_name_and_path(entrance)})")
      self.add_line("if o.carry_through_doors:")
      self.indent += 1
      self.define_rules(entrance.rule, "e")
      self.indent -= 1
      self.add_line("else:")
      self.indent += 1
      if entrance.rule is not None:
        self.define_rules(carrying.no_temp_items & entrance.rule, "e")
      else:
        self.define_rules(carrying.no_temp_items, "e")
      self.indent -= 1
      self.add_line(f"entrances[{entrance_name_and_path(entrance)}]=(e,{repr(entrance.is_dest_underwater)})")
    self.add_line("return entrances")

def generate_entrance_rando(first_line: str):
  with open("ap_generated/entrance_rando.py", "w") as out_py:
    _ = out_py.write(f"{first_line}\n")
    _ = out_py.write(EntranceRandoBuilder.build())
