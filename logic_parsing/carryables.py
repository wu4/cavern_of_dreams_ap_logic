from typing import Literal, TypeAlias

from ..logic.carrying import Carrying
from ..logic.logic import Logic, Not
from .helpers import dnf, get_carryings_from_logics, unique_only

CarryableKey: TypeAlias = Not | Carrying | Literal["dont-care"]

def distribute_carryable_logic(l: Logic) -> dict[CarryableKey, list[list[Logic]]]:
  logics_by_carryable: dict[CarryableKey, list[list[Logic]]] = {}
  d_or = list(map(list, dnf(l)))
  for d_and in d_or:
    unique_carryings = unique_only(get_carryings_from_logics(d_and))
    carrying = next(
      iter(sorted(
        unique_carryings,
        key=lambda x: isinstance(x, Carrying) and not (x.carryable is None)
      )),
      None
    )
    if carrying is not None:
      d_and = list(logic for logic in d_and if logic not in unique_carryings)
      group = carrying
    else:
      group = "dont-care"

    logics_by_carryable.setdefault(group, []).append(d_and)

  for group, rules in logics_by_carryable.items():
    if [] in rules:
      logics_by_carryable[group] = []

  return logics_by_carryable
