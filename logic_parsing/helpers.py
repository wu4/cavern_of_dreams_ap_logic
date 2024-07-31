from collections.abc import Iterable, Generator, Sequence
from typing import TypeAlias, TypeVar
from itertools import product as itertools_product

from ..logic.logic import ChainableLogic, Logic, Any, All, Not
from ..logic.option import AnyOption, Option
from ..logic.comment import Comment
from ..logic.carrying import Carrying

def enter_comments(l: Logic) -> Logic:
  if isinstance(l, Comment):
    return l.logic
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

def _or_dnf(l: Any):
  for e in l.operands:
    for se in dnf(e):
      yield se

def _and_dnf(l: All):
  for c in itertools_product(*[dnf(e) for e in l.operands]):
    yield list(enter_comments(se) for e in c for se in e)

def _dnf_helper(l: Logic) -> Sequence[Sequence[Logic]]:
  l = enter_comments(l)
  if not isinstance(l, (Any, All)):
    return [[l]]
  elif isinstance(l, Any):
    return list(_or_dnf(l))
  else:
    return list(_and_dnf(l))

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
      if isinstance(self.logic, ChainableLogic):
        operands = self.logic.operands
        branches_as_logic = list(filter(lambda x: x not in operands, branches_as_logic))
      return self.logic & Any(*unique_only(branches_as_logic))
    else:
      return self.logic

def simplify(in_lss: Sequence[Sequence[Logic]]) -> Any:
  ret: Sequence[Logic] = []

  # remove all supersets
  lss: list[list[Logic]] = list(map(list, filter(lambda ls: not any(map(lambda other_ls: set(ls).issuperset(set(other_ls)), filter(lambda x: ls != x, in_lss))), in_lss)))

  print("\033[31mUNIMPLEMENTED: SIMPLIFY\033[0m")
  return nested_list_to_logic(lss)

  if len(lss) <= 1:
    return nested_list_to_logic(lss)

  # set_ls = set(lss[0])
  # all_shared = set_ls.intersection(*map(set, lss[1:]))

  scores = get_simplification_scores(lss)

  chunks: Chunks = [set(range(0, len(lss)))]
  logics_by_chunks: dict[tuple[int, ...], list[Logic]] = {}
  # print(len(lss))
  # print(nested_list_to_logic(lss))
  # print(chunks)

  mismatched_chunks: dict[tuple[int, ...], list[Logic]] = {}

  for score, indices, logic in scores:
    indices_set = set(indices)
    # print(indices_set, logic)
    chunk = next(filter(indices_set.issubset, chunks), None)
    if chunk is None:
      mismatched_chunks.setdefault(tuple(sorted(indices)), []).append(logic)
      continue

    if chunk != indices_set:
      chunks.append(chunk - indices_set)
      chunk.clear()
      chunk.update(indices_set)

    logics_by_chunks.setdefault(tuple(sorted(indices)), []).append(logic)

  # print(mismatched_chunks)
  print("matched:")
  for indices, logic in logics_by_chunks.items():
    print(indices, Any(*logic))

  print("mismatched:")
  for indices, logic in mismatched_chunks.items():
    print(indices, Any(*logic))
    indices_set = set(indices)
    # print(indices_set, chunks)
    chunks_by_size = sorted(chunks, key=len)
    while indices_set:
      # print(indices_set, chunks_by_size)
      superset = next(filter(lambda chunk: any(map(lambda index: index in chunk, indices_set)), chunks_by_size), None)
      if superset is None:
        logics_by_chunks.setdefault(tuple(sorted(indices_set)), []).extend(logic)
        break
      common_indices = superset.intersection(indices_set)
      indices_set -= common_indices
      if common_indices != superset:
        if indices_set:
          chunks.append(common_indices)
          superset.clear()
          superset.update(indices_set)
        else:
          superset.clear()
      logics_by_chunks.setdefault(tuple(sorted(common_indices)), []).extend(logic)
  print("end mismatched")

  all_logics = sorted(
    ((k, Chunk(All(*logics_by_chunks[k]))) for k in logics_by_chunks.keys()),
    key=lambda x: len(x[0]),
    reverse=False
  )

  for indices, chunk in all_logics:
    print(indices, chunk.consume())

  seen: set[tuple[int, ...]] = set()

  subsets: set[tuple[int, ...]] = set()

  for indices, chunk in all_logics:
    if indices in seen: continue
    seen.add(indices)

    for other_indices, _other_logic in all_logics:
      if other_indices in seen: continue
      indices_set = set(indices)
      other_indices_set = set(other_indices)

      # find first superset only, which should be the largest possible due to
      # sorting
      if indices_set.issubset(other_indices_set):
        subsets.add(indices)
        next(filter(lambda x: x[0] == other_indices, all_logics))[1].add_branch(chunk)
        # accum.append(logic)
        break

  seen2: set[int] = set()
  for indices, chunk in reversed(all_logics):
    if not seen2.isdisjoint(indices): continue
    seen2.update(indices)
    ret.append(chunk.consume())

  return Any(*ret)

def nested_list_to_logic(lss: Sequence[Sequence[Logic]]) -> Any:
  return Any(*[All(*ls) for ls in lss])
