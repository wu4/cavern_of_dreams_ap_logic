# from typing import TypeAlias

from . import carrying
# from ..generated_types import abilityItem, nonVanillaAbilityItem, pickupItem
from .has import Collected

# HasItemType: TypeAlias = abilityItem | nonVanillaAbilityItem | pickupItem

# unused
# class Collected(has.Collected[HasItemType]):
#   pass

wings = Collected("Wings")
double_jump = Collected("Double Jump")
bubble = Collected("Bubble")
flight = Collected("Flight")
roll = Collected("Roll")
sprint = Collected("Sprint")
high_jump = Collected("High Jump")
swim = Collected("Swim")
carry = Collected("Carry")
air_swim = Collected("Air Swim")

fish_food = Collected("Fish Food")
lady_opal_egg_1 = Collected("Lady Opal's Egg 1")
lady_opal_egg_2 = Collected("Lady Opal's Egg 2")
lady_opal_egg_3 = Collected("Lady Opal's Egg 3")

horn = carrying.no_throwables & Collected("Horn")
air_tail = carrying.no_throwables & (Collected("Aerial Tail") | Collected("Tail"))
ground_tail = carrying.no_throwables & (Collected("Grounded Tail") | Collected("Tail"))
climb = carrying.no_throwables & Collected("Climb")
