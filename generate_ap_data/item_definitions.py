from collections.abc import Iterable
import re
from ..csv_parsing import read_locations_csv, FlagList, FlagListWithLocations

_snake_case_re = re.compile('([A-Z]+)')
def as_snake_case(camel_case: str) -> str:
  return _snake_case_re.sub(r'_\1', camel_case).lower()

def parse(location_datas: dict[str, FlagList]) -> Iterable[str]:
  accum: list[str] = []

  all_locations: dict[str, str] = {}
  all_items: dict[str, str] = {}

  for cat, flag_list in location_datas.items():
    snake_case_cat = as_snake_case(cat)

    all_items.update(flag_list.items)
    accum += serialize_list(flag_list.items.values(), f"{snake_case_cat}_items")

    if not isinstance(flag_list, FlagListWithLocations): continue

    all_locations.update(flag_list.locations)
    accum += serialize_list(flag_list.locations.values(), f"{snake_case_cat}_locations")

  accum += serialize_list(all_locations.values(), "all_locations")
  accum += serialize_list(all_items.values(), "all_items")

  accum += serialize_dict({all_items[flag_name[9:]]: location_name for flag_name, location_name in all_locations.items()}, "vanilla_locations")

  return accum

def serialize_dict(items: dict[str, str], name: str) -> list[str]:
  return [
    f"{name}:dict[str,str]=" + "{",
    *(f'"{k}":"{v}",' for k, v in items.items()),
    "}"
  ]

def serialize_list(items: Iterable[str], name: str) -> list[str]:
  return [
    f"{name}:list[str]=[",
    *(f'"{i}",' for i in items),
    "]"
  ]

def generate():
  """Assumes working directory is cavern_of_dreams_ap_logic"""

  accum: list[str] = []

  location_datas = read_locations_csv("location_names.csv")
  accum.append("# Generated using cavern_of_dreams_ap_logic/generate_ap_data")
  accum += parse(location_datas)
  with open("ap_generated/data.py", "w") as out_py:
    _ = out_py.write("\n".join(accum))
