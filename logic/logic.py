from __future__ import annotations
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Callable, Generic, TypeAlias, TypeVar, override

class Logic(metaclass=ABCMeta):
  def __and__(self, other: Logic) -> All:
    return All(self, other)

  def __or__(self, other: Logic) -> Any:
    return Any(self, other)

  def __invert__(self) -> Not:
    return Not(self)

  @abstractmethod
  def into_server_code(self) -> str:
    """Function for converting logic into code for the server-side in Python."""
    ...

T = TypeVar("T")

def splitter(data: list[T], pred: Callable[[T], bool]) -> tuple[list[T], list[T]]:
  yes: list[T] = []
  no: list[T] = []
  for d in data:
    (yes if pred(d) else no).append(d)
  return (yes, no)

if TYPE_CHECKING:
  from .has import CollectedAny
  from .carrying import Carrying

def list_as_str_set(a: list[str | None]):
  return "{" + repr(a)[1:-1] + "}"

def serialize_collecteds(collecteds: Iterable["CollectedAny"]) -> str:
  return repr([str(x.item) for x in collecteds])

def serialize_carryings(carryings: Iterable["Carrying"]) -> str:
  return f"s._cavernofdreams_carrying[p] in {list_as_str_set([x.carryable for x in carryings])}"

class ChainableLogic(Logic):
  server_code_separator: str = ""
  server_code_function: str = ""
  operands: list[Logic]

  def __init__(self, *args: Logic) -> None:
    super().__init__()
    unwrapped: list[Logic] = []
    for item in args:
      if isinstance(item, self.__class__):
        unwrapped.extend(item.operands)
      else:
        unwrapped.append(item)
    self.operands = unwrapped

  @override
  def into_server_code(self) -> str:
    from .has import Collected
    logics: list[str] = []
    collected_operands, other_operands = splitter(self.operands, lambda x: isinstance(x, Collected))
    from .carrying import Carrying
    carrying_operands, other_operands = splitter(other_operands, lambda x: isinstance(x, Carrying))
    co_len = len(collected_operands)
    cr_len = len(carrying_operands)
    if cr_len == 1:
      logics.append(carrying_operands[0].into_server_code())
    elif cr_len > 1:
      logics.append(serialize_carryings(carrying_operands)) # pyright: ignore[reportArgumentType]

    if co_len == 1:
      logics.append(collected_operands[0].into_server_code())
    elif co_len > 1:
      # pythons typing system doesnt support type narrowing here
      # cast technically has a performance cost, but comments dont! :3

      # collected_operands is guaranteed to be list[CollectedAny]
      serialized = serialize_collecteds(collected_operands) # pyright: ignore[reportArgumentType]

      logics.append(f"s.{self.server_code_function}({serialized}, p)")

    if len(other_operands) > 0:
      for op in other_operands:
        logics.append(op.into_server_code())

    # the use of spaces is intentional
    return "(" + f" {self.server_code_separator} ".join(logics) + ")"

class All(ChainableLogic):
  server_code_separator = "and"
  server_code_function = "has_all"

  @override
  def __str__(self) -> str:
    return "(" + " && ".join(map(str, self.operands)) + ")"

class Any(ChainableLogic):
  server_code_separator = "or"
  server_code_function = "has_any"

  @override
  def __str__(self) -> str:
    return "(" + (" || ".join(map(str, self.operands))) + ")"

class Not(Logic):
  @override
  def __str__(self) -> str:
    return f"Not {self.logic}"

  def __init__(self, logic: Logic) -> None:
    super().__init__()
    self.logic = logic

  @override
  def into_server_code(self) -> str:
    return f"not ({self.logic.into_server_code()})"

MaybeLogic: TypeAlias = Logic | None
