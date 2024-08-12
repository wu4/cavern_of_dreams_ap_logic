import subprocess

from .entrance_rando import generate_entrance_rando
from .item_definitions import generate as generate_item_definitions
from .regions import generate as generate_regions

def switch_to_this_script_parent_dir():
  """
  Changes working directory to *above* the containing directory of this script.
  Should ALWAYS be cavern_of_dreams_ap_logic.
  """
  import os
  dirname = os.path.dirname
  abspath = os.path.abspath

  os.chdir(dirname(dirname(abspath(__file__))))


if __name__ == "__main__":
  switch_to_this_script_parent_dir()

  subprocess.check_call(["git", "update-index", "--refresh"])
  subprocess.check_call(["git", "diff-index", "--quiet", "HEAD", "--"])
  exitcode, commit_hash = subprocess.getstatusoutput("git rev-parse --short HEAD")

  first_line = f"# generated from cavern_of_dreams_ap_logic @ {commit_hash}"

  generate_item_definitions(first_line)
  generate_regions(first_line)
  generate_entrance_rando(first_line)
