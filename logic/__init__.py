from __future__ import annotations
from abc import abstractmethod
from typing import TypeAlias, override

class Logic:
  def __and__(self, other: Logic) -> All:
    return All(self, other)

  def __or__(self, other: Logic) -> Any:
    return Any(self, other)

  @abstractmethod
  def into_server_code(self) -> str:
    """Function for converting logic into code for the server-side in Python."""
    ...
    # raise NotImplementedError()

class ChainableLogic(Logic):
  server_code_separator: str = ""

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
    return "(" + f" {self.server_code_separator} ".join(map(lambda op: op.into_server_code(), self.operands)) + ")"

class All(ChainableLogic):
  server_code_separator = "and"

  @override
  def __str__(self) -> str:
    return "(" + " && ".join(map(str, self.operands)) + ")"

class Any(ChainableLogic):
  server_code_separator = "or"

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

from .objects import *
