from __future__ import annotations
from .levels import data as level_data
from .type import CollectionState
from typing import TypeAlias, Callable

from dataclasses import dataclass

def set_rules(self: World):
    p = self.player
    o = self.options


    shroomsanity = o.shroomsanity.value > 0
    cardsanity = o.cardsanity.value > 0

    # tailless = o.tailless.value > 0
