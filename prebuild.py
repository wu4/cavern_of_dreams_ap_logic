import csv
from dataclasses import dataclass

@dataclass
class LocationData:
    pretty_name: str
    flag_name: str
    item_name: str

if __name__ == "__main__":
    accum: list[str] = []
    location_datas: dict[str, list[LocationData]] = {}
    with open("location_names.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        current_category: str | None = None
        for row in reader:
            if len(row) == 1:
                current_category = row[0]
                location_datas[current_category] = []
                continue

            location_datas[str(current_category)].append(LocationData(row[1], row[2], row[0]))

    accum.append(f"all_locations: list[str]=" "[")
    for (category, datas) in location_datas.items():
        for data in datas:
            accum.append(f'"{data.pretty_name}",')
    accum.append("]")

    for (category, datas) in location_datas.items():
        accum.append(f"{category}_locations: list[str]=" "[")
        for data in datas:
            accum.append(f'"{data.pretty_name}",')
        accum.append("]")

    accum.append(f"all_items: list[str]=" "[")
    for (category, datas) in location_datas.items():
        if category == "shroom":
            accum.append('"Shroom",')
            continue

        for data in datas:
            accum.append(f'"{data.item_name}",')
    accum.append("]")

    for (category, datas) in location_datas.items():
        if category == "shroom":
            accum.append(f"shroom_count: int={len(datas)}")
        else:
            accum.append(f"{category}_items: list[str]=" "[")
            for data in datas:
                accum.append(f'"{data.item_name}",')
            accum.append("]")

    accum.append(f"vanilla_locations: dict[str, str]=" "{")
    for (category, datas) in location_datas.items():
        for data in datas:
            accum.append(f'"{data.pretty_name}": "{data.item_name}",')
    accum.append("}")

    with open("level.pyt", "w") as out_py:
        out_py.write("\n".join(accum))