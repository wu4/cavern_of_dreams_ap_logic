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

    generate_item_definitions()
    generate_regions()
