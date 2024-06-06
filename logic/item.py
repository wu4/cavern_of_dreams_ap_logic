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

horn = carrying.no_throwables & Collected("Horn")
air_tail = carrying.no_throwables & Collected("Aerial Tail")
ground_tail = carrying.no_throwables & Collected("Grounded Tail")
climb = carrying.no_throwables & Collected("Climb")
