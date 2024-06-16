from csv_parsing import read_locations_csv, parse, FlagListIteration


def serialize(item: FlagListIteration) -> list[str]:
    ret: list[str] = []
    name = f"{item.category}{
        item.type}" if item.category is not None else f"Any{item.type}"
    ret.append(f"{name}: TypeAlias = Literal[")

    for item_name in item.flag_list.values():
        ret.append(f'"{item_name}",')

    ret.append("]")
    return ret


if __name__ == "__main__":
    accum: list[str] = []

    location_datas = read_locations_csv("location_names.csv")
    accum.append("# Generated using prebuild.py")
    accum.append("from typing import TypeAlias, Literal")
    accum += parse(location_datas, serialize)
    with open("generated.py", "w") as out_py:
        _ = out_py.write("\n".join(accum))
