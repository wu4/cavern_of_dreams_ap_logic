from .option import Option
# from typing import TypeAlias

from . import carrying
# from ..generated_types import abilityItem, nonVanillaAbilityItem, pickupItem
from .has import Collected

# HasItemType: TypeAlias = abilityItem | nonVanillaAbilityItem | pickupItem

# unused
# class Collected(has.Collected[HasItemType]):
#   pass

double_jump = Collected("Double Jump") & Option("include_double_jump")
flight = Collected("Flight") & Option("exclude_flight", 0)
air_swim = Collected("Air Swim") & Option("air_swim", 1, True)

wings = Collected("Wings") & Option("exclude_wings", 0)
bubble = Collected("Bubble")
roll = Collected("Roll")
sprint = Collected("Sprint")
high_jump = Collected("High Jump")
swim = Collected("Swim")
carry = Collected("Carry")

fish_food = Collected("Fish Food")
lady_opal_egg_1 = Collected("Lady Opal's Egg 1")
lady_opal_egg_2 = Collected("Lady Opal's Egg 2")
lady_opal_egg_3 = Collected("Lady Opal's Egg 3")

horn = carrying.no_throwables & Collected("Horn")
air_tail = carrying.no_throwables & ((Option("split_tail") & Collected("Aerial Tail")) | (Option("split_tail", 0) & Collected("Tail")))
ground_tail = carrying.no_throwables & ((Option("split_tail") & Collected("Grounded Tail")) | (Option("split_tail", 0) & Collected("Tail")))
climb = carrying.no_throwables & Collected("Climb")
