from collections.abc import Iterable, Mapping
import re

from ..logic.objects import CarryableLocation
# from ..csv_parsing import read_locations_csv, FlagList, FlagListWithLocations
from .. import all_locations
from .connection_parser import all_regions

_snake_case_re = re.compile('([A-Z]+)')
def as_snake_case(camel_case: str) -> str:
  return _snake_case_re.sub(r'_\1', camel_case).lower()

# def parse(location_datas: dict[str, FlagList]) -> Iterable[str]:
#   accum: list[str] = []
# 
#   all_locations: dict[str, str] = {}
#   all_items: dict[str, str] = {}
# 
#   for cat, flag_list in location_datas.items():
#     snake_case_cat = as_snake_case(cat)
# 
#     all_items.update(flag_list.items)
#     accum += serialize_list(flag_list.items.values(), f"{snake_case_cat}_items")
# 
#     if not isinstance(flag_list, FlagListWithLocations): continue
# 
#     all_locations.update(flag_list.locations)
#     accum += serialize_list(flag_list.locations.values(), f"{snake_case_cat}_locations")
# 
#   accum += serialize_list(all_locations.values(), "all_locations")
#   accum += serialize_list(all_items.values(), "all_items")
# 
#   accum += serialize_dict({all_items[flag_name[9:]]: location_name for flag_name, location_name in all_locations.items()}, "vanilla_locations")
# 
#   return accum


def serialize_dict(items: Mapping[str, object], name: str) -> list[str]:
  return [
    f"{name}:dict[str,str]=" + "{",
    *(f'{repr(k)}:{repr(v)},' for k, v in items.items()),
    "}"
  ]


def serialize_list(items: Iterable[str], name: str) -> list[str]:
  return [
    f"{name}:list[str]=[",
    *(f'{repr(i)},' for i in items),
    "]"
  ]

def get_vanilla_locations():
  ret: dict[str, str] = {}
  for _name, cat in all_locations.all_categories():
    if not isinstance(cat, all_locations.Category): continue
    for i in cat.rows:
      ret[i.location] = i.item
  return ret

def generate():
  """Assumes working directory is cavern_of_dreams_ap_logic"""

  accum: list[str] = []

  for name, cat in all_locations.all_categories():
    snake_case_cat = as_snake_case(name)
    accum += serialize_list((x.item for x in cat.rows), f"{snake_case_cat}_items")
    if not isinstance(cat, all_locations.Category): continue
    accum += serialize_list((x.location for x in cat.rows), f"{snake_case_cat}_locations")

  accum += serialize_list(all_locations.all_locations(), "all_locations")
  accum += serialize_list(all_locations.all_items(), "all_items")
  accum += serialize_dict(get_vanilla_locations(), "vanilla_locations")
  accum += serialize_dict({v: k for k, v in get_vanilla_locations().items()}, "vanilla_locations_by_name")


  accum.append("item_groups:dict[str,list[str]]={")
  for name, cat in all_locations.all_categories():
    capital = name[0].upper() + name[1:]
    accum.append(repr(capital) + ":[")
    accum.extend(repr(i.item) + "," for i in cat.rows)
    accum.append("],")
  accum.append("}")
  accum.append("item_group_sets:dict[str,set[str]]={group:set(ls) for group,ls in item_groups.items()}")

  carryable_locations: dict[str, str | None] = {}

  for region in all_regions:
    for location in region.locations.keys():
      if isinstance(location, str): continue
      if not issubclass(location, CarryableLocation): continue
      carryable_locations[str(location)] = location.carryable

  carryable_locations["dont-care"] = None
  accum += serialize_dict(carryable_locations, "carryable_locations")

  # location_datas = read_locations_csv("location_names.csv")
  accum.append("# Generated using cavern_of_dreams_ap_logic/generate_ap_data")
  # accum += parse(location_datas)
  with open("ap_generated/data.py", "w") as out_py:
    _ = out_py.write("\n".join(accum))
