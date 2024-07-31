from typing import Literal, TypeAlias

from ..logic.carrying import Carrying
from ..logic.logic import Logic, Not
from .helpers import dnf, get_carryings_from_logics

CarryableKey: TypeAlias = Not | Carrying | Literal["dont-care"]

def distribute_carryable_logic(l: Logic) -> dict[CarryableKey, list[list[Logic]]]:
  logics_by_carryable: dict[CarryableKey, list[list[Logic]]] = {}
  d_or = list(map(list, dnf(l)))
  for d_and in d_or:
    carrying = next(get_carryings_from_logics(d_and), None)
    if carrying is not None:
      d_and = list(filter(carrying.__ne__, d_and))
      group = carrying
    else:
      group = "dont-care"

    logics_by_carryable.setdefault(group, []).append(d_and)

  for group, rules in logics_by_carryable.items():
    if [] in rules:
      logics_by_carryable[group] = []

  return logics_by_carryable
