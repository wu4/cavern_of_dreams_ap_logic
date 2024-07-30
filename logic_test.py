from .logic_parsing.helpers import simplify, nested_list_to_logic
from .logic_parsing.carryables import distribute_carryable_logic
from .levels.CAVE.SunCavern import Main, DucklingsDoorway
# from .levels.GALLERY.WaterLobby import Spooky

Main.lazy_load()
logic_to_test = Main.region_connections[DucklingsDoorway]
# logic_to_test = Spooky.locations["Gallery of Nightmares - Sewer Angel Statue Puzzle"]
assert logic_to_test is not None

for kind, rules in distribute_carryable_logic(logic_to_test).items():
  print(f"\033[33m{kind}\033[0m")
  print(f"\033[33mBEFORE:\033[0m")
  print(nested_list_to_logic(rules))
  print(f"\033[33mAFTER:\033[0m")
  print(simplify(rules))
