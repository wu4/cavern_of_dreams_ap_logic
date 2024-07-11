from ...logic import lazy_region, Region, Entrance
from ...logic import event

area_path = "PALACE/Observatory"

class ValleyDoor(Entrance):
  warp_path = f"{area_path}/Warps/WarpFromObservatoryToPalace"
  dest_path = f"{area_path}/Warps/DestFromPalaceToObservatory"

@lazy_region
def Main(r: Region):
  r.locations = {
    "Card: Observatory": None,
    "Egg: Observatory": event.Collected("Reveal Observatory Item"),
    "Observatory - Telescope Puzzle": None
  }

  from . import Valley

  r.entrances = [
    ValleyDoor.define(Valley.ObservatoryDoor)
  ]
