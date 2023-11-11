from ..shared import Area

def get_levels() -> dict[str, dict[str, Area]]:
  from pathlib import Path
  from importlib import import_module

  ret = {}
  this_package = Path(__file__).resolve().as_posix()
  for f in Path(__file__, "..", "levels").iterdir():
    module_name = f.stem
    if module_name == "__init__": continue
    ret[module_name] = import_module(f"levels.{module_name}", this_package).data

  return ret

data = get_levels()