from collections.abc import Sequence
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
