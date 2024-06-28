import csv
from dataclasses import dataclass
from typing import Callable, Literal, cast
from collections.abc import Iterable

@dataclass
class CheckData:
    item_name: str
    flag_name: str

@dataclass
class CheckDataWithLocation(CheckData):
    location_name: str

class FlagList:
    def __init__(self, datas: Iterable[CheckData]) -> None:
        super().__init__()
        self.items: dict[str, str] = {}
        for data in datas:
            self.items[data.flag_name] = data.item_name

class FlagListWithLocations(FlagList):
    def __init__(self, datas: Iterable[CheckDataWithLocation]):
        super().__init__(datas)

        self.locations: dict[str, str] = {}

        for data in datas:
            self.locations[f"LOCATION_{data.flag_name}"] = data.location_name

@dataclass
class FlagListIteration:
    flag_list: dict[str, str]
    category: str | None
    type: Literal["Location", "LocationByName", "Item", "ItemByName"]

def parse(
        location_datas: dict[str, FlagList],
        serialize_func: Callable[[FlagListIteration], list[str]],
        include_by_name: bool = False
    ) -> Iterable[str]:
    accum: list[str] = []

    all_locations: dict[str, str] = {}
    all_items: dict[str, str] = {}

    for cat, flag_list in location_datas.items():
        if isinstance(flag_list, FlagListWithLocations):
            all_locations.update(flag_list.locations)
            accum += serialize_func(FlagListIteration(flag_list.locations, cat, "Location"))
            if include_by_name:
                accum += serialize_func(FlagListIteration({v: k for k, v in flag_list.locations.items()}, cat, "LocationByName"))

        all_items.update(flag_list.items)
        accum += serialize_func(FlagListIteration(flag_list.items, cat, "Item"))
        if include_by_name:
            accum += serialize_func(FlagListIteration({v: k for k, v in flag_list.items.items()}, cat, "ItemByName"))

    accum += serialize_func(FlagListIteration(all_locations, None, "Location"))
    accum += serialize_func(FlagListIteration(all_items, None, "Item"))
    if include_by_name:
        accum += serialize_func(FlagListIteration({v: k for k, v in all_locations.items()}, None, "LocationByName"))
        accum += serialize_func(FlagListIteration({v: k for k, v in all_items.items()}, None, "ItemByName"))

    return accum

def read_locations_csv(filename: str) -> dict[str, FlagList]:
    location_datas: dict[str, FlagList] = {}

    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        current_category: str | None = None
        accum: list[CheckData] = []
        has_locations = False
        def consume_category():
            if current_category is not None:
                location_datas[current_category] = FlagListWithLocations(cast(list[CheckDataWithLocation], accum)) if has_locations else FlagList(accum)

        # skip header line
        _ = reader.__next__()

        for row in reader:
            if len(row) == 0:
              continue
            if len(row) != 3:
              raise Exception(row)
            elif row[1] == "" and row[2] == "":
                consume_category()
                current_category = row[0]
                accum = []
                continue
            elif row[1] == "":
                has_locations = False
                accum.append(CheckData(row[0], row[2]))
            else:
                has_locations = True
                accum.append(CheckDataWithLocation(row[0], row[2], row[1]))

        consume_category()

    return location_datas
