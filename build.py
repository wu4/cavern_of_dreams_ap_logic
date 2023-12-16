import json
from yaml import load
try:
  from yaml import CLoader as Loader
except ImportError:
  from yaml import Loader
from pathlib import Path

"""
import csv
from dataclasses import dataclass
from typing import TypeAlias

@dataclass
class LocationData:
    pretty_name: str
    flag_name: str
    item_name: str

LocationDatas: TypeAlias = dict[str, list[LocationData]]

def get_location_datas() -> LocationDatas:
  location_datas: LocationDatas = {}

  with open("location_names.csv", "r") as csv_file:
      reader = csv.reader(csv_file)
      current_category: str | None = None
      for row in reader:
          if len(row) == 0:
              continue
          if len(row) == 1:
              current_category = row[0]
              location_datas[current_category] = []
              continue

          location_datas[str(current_category)].append(LocationData(row[1], row[2], row[0]))

  return location_datas

def write_eventitems(datas: LocationDatas):
  accum: list[str] = []

  accum.append("description: An event")
  accum.append("minProperties: 1")
  accum.append("maxProperties: 1")
  accum.append("properties:")

  for data in datas["event"]:
    accum.append(f" \"{data.item_name}\": ./logic.yaml")

  with open("schema/_generated_eventitem.yaml", "w") as file:
    file.write("\n".join(accum))

def truncate_name(name: str) -> str:
  ind = name.find(" - ")
  if ind >= 0:
    return name[ind+3:]
  else:
    return name

def write_eventlocs(datas: LocationDatas):
  accum: list[str] = []

  accum.append("description: The original location of an event")
  accum.append("minProperties: 1")
  accum.append("maxProperties: 1")
  accum.append("properties:")

  unique = set(map(lambda x: truncate_name(x.pretty_name), datas["event"]))

  for name in unique:
    accum.append(f" \"{name}\": ./logic.yaml")

  with open("schema/_generated_eventlocation.yaml", "w") as file:
    file.write("\n".join(accum))
"""

import os
if __name__ == "__main__":
  levels: dict = {}
  for folder_name in os.listdir("levels"):
    level_name: str = Path(folder_name).stem
    for file_name in os.listdir(f"levels/{folder_name}"):
      room_name: str = Path(file_name).stem
      with open(f"levels/{folder_name}/{file_name}", "r") as file:
        levels.setdefault(level_name, {})[room_name] = load(stream=file, Loader=Loader)
  
  with open("levels.json", "w") as out:
    json.dump(levels, out)

  # datas = get_location_datas()
  # write_eventitems(datas)
  # write_eventlocs(datas)