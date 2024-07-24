import all_locations

if __name__ == "__main__":
    accum: list[str] = []

    accum.append("# Generated using prebuild.py")
    accum.append("from typing import TypeAlias, Literal")

    accum.extend(all_locations.generate_item_lines(
      lambda category: f"{category}Item:TypeAlias=Literal[",
      lambda item: repr(item) + ",",
      "]"
    ))

    accum.extend(all_locations.generate_location_lines(
      lambda category: f"{category}Location:TypeAlias=Literal[",
      lambda location: repr(location) + ",",
      "]"
    ))
    with open("generated_types.py", "w") as out_py:
        _ = out_py.write("\n".join(accum))
