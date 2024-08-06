from collections.abc import Sequence
from typing import Literal, TypeAlias
from ..logic.logic import Logic
from ..logic.option import AnyOption
from .helpers import cleanup, dnf, get_options_from_logics

def get_required_options(l: Logic) -> Sequence[Sequence[AnyOption]]:
  d = dnf(l)
  options: Sequence[Sequence[AnyOption]] = []
  for o in d:
    options_list = list(get_options_from_logics(o))

    if len(options_list) == 0:
      # there exists a logical path that doesnt require any options
      return []

    options.append(options_list)

  return cleanup(options)

OptionKey: TypeAlias = set[AnyOption] | Literal["dont-care"]

def distribute_logic_by_options(l: Logic) -> list[tuple[OptionKey, list[list[Logic]]]]:
  logics_by_option: list[tuple[OptionKey, list[list[Logic]]]] = []

  def add_branch(key: OptionKey, branch: list[Logic]):
    i = next((i for i, (o_key, _ls) in enumerate(logics_by_option) if o_key == key), None)
    if i is None:
      logics_by_option.append((key, [branch]))
    else:
      logics_by_option[i][1].append(branch)

  d_or = list(map(list, dnf(l)))
  for d_and in d_or:
    options = set(get_options_from_logics(d_and))
    if options:
      d_and = list(logic for logic in d_and if logic not in options)
      group = options
    else:
      group = "dont-care"

    add_branch(group, d_and)

  for i, (group, rules) in enumerate(logics_by_option):
    if [] in rules:
      logics_by_option[i] = (group, [])

  return logics_by_option
