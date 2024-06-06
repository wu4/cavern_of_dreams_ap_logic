from collections.abc import Iterable

from .csv_parsing import read_locations_csv, FlagList, FlagListWithLocations

def parse(location_datas: dict[str, FlagList]) -> Iterable[str]:
    accum: list[str] = []

    all_locations: dict[str, str] = {}
    all_items: dict[str, str] = {}

    for cat, flag_list in location_datas.items():
        if isinstance(flag_list, FlagListWithLocations):
            all_locations.update(flag_list.locations)
            accum += serialize_list(flag_list.locations.values(), f"{cat}_locations")

        all_items.update(flag_list.items)
        accum += serialize_list(flag_list.items.values(), f"{cat}_items")

    accum += serialize_list(all_locations.values(), "all_locations")
    accum += serialize_list(all_items.values(), "all_items")

    accum += serialize_dict({all_items[flag_name[9:]]: location_name for flag_name, location_name in all_locations.items()}, "vanilla_locations")

    return accum

def serialize_dict(items: dict[str, str], name: str) -> list[str]:
    ret: list[str] = []

    ret.append(f"{name}:dict[str,str]=" + "{")

    for k, v in items.items():
        ret.append(f'"{k}":"{v}",')

    ret.append("}")
    return ret

def serialize_list(items: Iterable[str], name: str) -> list[str]:
    ret: list[str] = []

    ret.append(f"{name}:list[str]=[")

    for i in items:
        ret.append(f'"{i}",')

    ret.append("]")
    return ret

if __name__ == "__main__":
    accum: list[str] = []

    location_datas = read_locations_csv("location_names.csv")
    accum.append("# Generated using cavern_of_dreams_ap_logic/generate_data.py")
    accum += parse(location_datas)
    with open("ap_generated/data.py", "w") as out_py:
        _ = out_py.write("\n".join(accum))
