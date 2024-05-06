from __future__ import annotations
from typing import TypeAlias

class Logic:
  def __and__(self, other: Logic) -> All:
    return All(self, other)

  def __or__(self, other: Logic) -> Any:
    return Any(self, other)

class ChainableLogic(Logic):
  def __init__(self, *args: Logic) -> None:
    super().__init__()
    unwrapped: list[Logic] = []
    for item in args:
      if isinstance(item, self.__class__):
        unwrapped.extend(item.operands)
      else:
        unwrapped.append(item)
    self.operands = unwrapped

class All(ChainableLogic):
  def __str__(self) -> str:
    return "(" + (" && ".join(map(str, self.operands))) + ")"

class Any(ChainableLogic):
  def __str__(self) -> str:
    return "(" + (" || ".join(map(str, self.operands))) + ")"
  
class Not(Logic):
  def __str__(self) -> str:
    return f"Not {self.logic}"

  def __init__(self, logic: Logic) -> None:
    self.logic = logic

MaybeLogic: TypeAlias = Logic | None

from .objects import *