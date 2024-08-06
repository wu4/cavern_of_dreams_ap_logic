from collections.abc import Iterable, Generator, Sequence
from typing import TypeAlias, TypeVar
from itertools import product as itertools_product

from ..logic.logic import ChainableLogic, Logic, Any, All, Not
from ..logic.option import AnyOption, Option
from ..logic.comment import Comment
from ..logic.carrying import Carrying

def enter_comments(l: Logic) -> Logic:
  if isinstance(l, Comment):
    return enter_comments(l.logic)
  return l

T = TypeVar("T")

def unique_only(ts: Iterable[T]) -> Sequence[T]:
  ret: list[T] = []
  for t in ts:
    if not t in ret:
      ret.append(t)
  return ret

def get_carryings_from_logics(ls: Sequence[Logic]):
  for l in ls:
    if isinstance(l, Not):
      if not isinstance(l.logic, Carrying): continue
      yield l
    if not isinstance(l, Carrying): continue
    yield l

def get_options_from_logics(ls: Sequence[Logic]) -> Generator[AnyOption, None, None]:
  for l in ls:
    if not isinstance(l, Option): continue
    yield l

def is_valid_logic(ls: Sequence[Logic]):
  """
  If the logic asks for carrying multiple different carryables, it is not
  valid.
  """
  unique_carryables = unique_only(get_carryings_from_logics(ls))
  return len(unique_carryables) <= 1

def cleanup(lss: Sequence[Sequence[Logic]]) -> Sequence[Sequence[Logic]]:
  return unique_only(filter(is_valid_logic, lss))

def _flatten_nests(type_: type[ChainableLogic], logic: ChainableLogic):
  """
  Any(Any(...), ...) -> Any(...)

  All(All(...), ...) -> All(...)
  """
  ret: list[Logic] = []
  for inner_logic in logic.operands:
    inner_logic = enter_comments(inner_logic)
    if isinstance(inner_logic, type_):
      ret.extend(_flatten_nests(type_, inner_logic))
    elif isinstance(inner_logic, ChainableLogic):
      inner_logic_type = type(inner_logic)
      ret.append(inner_logic_type(*_flatten_nests(inner_logic_type, inner_logic)))
    else:
      ret.append(inner_logic)
  return ret

def _or_dnf(l: Any):
  ls = _flatten_nests(Any, l)

  for logic in ls:
    logic = enter_comments(logic)
    for se in dnf(logic):
      yield se

def _and_dnf(l: All):
  ls = _flatten_nests(All, l)

  for c in itertools_product(*[dnf(e) for e in ls]):
    yield list(enter_comments(se) for e in c for se in e)

def _dnf_helper(l: Logic) -> Sequence[Sequence[Logic]]:
  l = enter_comments(l)
  if isinstance(l, Any):
    return list(_or_dnf(l))
  elif isinstance(l, All):
    return list(_and_dnf(l))
  else:
    return [[l]]

def dnf(l: Logic) -> Sequence[Sequence[Logic]]:
  """
  Returns the disjunctive normal form (OR of ANDs) of some Logic, in the form
  of a nested list of Logics.
  """
  result = _dnf_helper(l)
  return list(cleanup(result))

def get_simplification_scores(lss: Sequence[Sequence[Logic]]) -> list[tuple[int, list[int], Logic]]:
  all_logics: list[Logic] = list(l for ls in lss for l in ls)

  ret: list[tuple[int, list[int], Logic]] = []

  for logic in unique_only(all_logics):
    indices = list(map(lambda x: x[0], filter(lambda x: logic in x[1], enumerate(lss))))
    ret.append((all_logics.count(logic), indices, logic))

  return sorted(ret, key=lambda x: -x[0])

Chunks: TypeAlias = list[set[int]]

def unwrap_all(a: Logic) -> Logic:
  if isinstance(a, All):
    if len(a.operands) == 1:
      return unwrap_all(a.operands[0])
  return a

class Chunk:
  logic: Logic
  branches: list["Chunk"]

  def __init__(self, logic: Logic):
    super().__init__()
    self.logic = unwrap_all(logic)
    self.branches = []

  def add_branch(self, chunk: "Chunk"):
    self.branches.append(chunk)

  def consume(self) -> Logic:
    branches_as_logic = list(map(lambda branch: branch.consume(), self.branches))
    if len(branches_as_logic) > 1:
      if isinstance(self.logic, Any):
        branches_as_logic = (x for x in branches_as_logic if x not in self.logic.operands)
      return self.logic & Any(*unique_only(branches_as_logic))
    elif len(branches_as_logic) == 1:
      return self.logic & branches_as_logic[0]
    else:
      return self.logic

def remove_redundancies(in_lss: Sequence[Sequence[Logic]]):
  return [
    ls for ls in in_lss
    if not any(set(ls).issuperset(set(other_ls)) for other_ls in in_lss if ls != other_ls)
  ]

def simplify(dnf_lss: Sequence[Sequence[Logic]]) -> Any:
  ret: Sequence[Logic] = []

  lss = remove_redundancies(dnf_lss)

  if len(lss) <= 1:
    return nested_list_to_logic(lss)

  scores = get_simplification_scores(lss)

  chunks: Chunks = [set(range(0, len(lss)))]
  logics_by_chunks: dict[tuple[int, ...], list[Logic]] = {}

  # mismatched_chunks: dict[tuple[int, ...], list[Logic]] = {}

  for score, indices, logic in scores:
    indices_set = set(indices)
    # print(indices_set, logic)
    chunk = next(filter(indices_set.issubset, chunks), None)
    if chunk is None:
      while indices_set:
        for chunk in chunks:
          intersection = indices_set.intersection(chunk)
          if not intersection: continue
          indices_set -= intersection
          if chunk != intersection:
            chunks.append(chunk - intersection)
            chunk.clear()
            chunk.update(intersection)
          logics_by_chunks.setdefault(tuple(sorted(intersection)), []).append(logic)
      continue

    if chunk != indices_set:
      chunks.append(chunk - indices_set)
      chunk.clear()
      chunk.update(indices_set)

    logics_by_chunks.setdefault(tuple(sorted(indices)), []).append(logic)

  # for indices, logic in mismatched_chunks.items():
  #   indices_set = set(indices)
  #   chunks_by_size = sorted(chunks, key=len)
  #   while indices_set:
  #     superset = next(filter(lambda chunk: any(map(lambda index: index in chunk, indices_set)), chunks_by_size), None)
  #     if superset is None: break

  #     common_indices = superset.intersection(indices_set)
  #     indices_set -= common_indices
  #     if indices_set:
  #       chunks.append(common_indices)
  #       superset.clear()
  #       superset.update(indices_set)

  #     logics_by_chunks.setdefault(tuple(sorted(common_indices)), []).extend(logic)

  all_logics = sorted(
    ((k, Chunk(All(*logics_by_chunks[k]))) for k in logics_by_chunks.keys()),
    key=lambda x: len(x[0]),
    reverse=True
  )

  from itertools import islice
  all_logics_len = len(all_logics)
  for i, (bigger_indices, bigger_chunk) in enumerate(all_logics):
    # print(bigger_indices, bigger_chunk.consume())
    if i == all_logics_len: break

    bigger_indices_set = set(bigger_indices)

    for smaller_indices, smaller_chunk in islice(all_logics, i+1, None):
      smaller_indices_set = set(smaller_indices)
      if not bigger_indices_set.intersection(smaller_indices_set): continue
      bigger_indices_set -= smaller_indices_set
      bigger_chunk.add_branch(smaller_chunk)
      if not bigger_indices_set: break

  seen2: set[int] = set()
  for bigger_indices, bigger_chunk in all_logics:
    if not seen2.isdisjoint(bigger_indices): continue
    seen2.update(bigger_indices)
    ret.append(bigger_chunk.consume())

  # dnf_ret = dnf(Any(*ret))
  # for logics in lss:
  #   if set(logics) in map(set, dnf_ret): continue
  #   print([str(logic) for logic in logics])

  return Any(*ret)

def nested_list_to_logic(lss: Sequence[Sequence[Logic]]) -> Any:
  return Any(*[All(*ls) for ls in lss])
