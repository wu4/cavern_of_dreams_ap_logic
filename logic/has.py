from __future__ import annotations
from typing import Generic, Literal, TypeAlias, override, TypeVar

from ..generated_types import AnyItem
from .objects import InternalEvent
from .logic import Logic

CarryingItem: TypeAlias = Literal[
  "Apple",
  "Medicine",
  "Bubble Conch",
  "Sage's Gloves",
  "Lady Opal's Head",
  "Shelnert's Fish",
  "Mr. Kerrington's Wings",
]

I = TypeVar("I", bound=AnyItem | type[InternalEvent] | CarryingItem)

class Collected(Logic, Generic[I]):
  item: I

  @override
  def __str__(self) -> str:
    return f"Has {self.item}"

  @override
  def into_server_code(self) -> str:
    return f"s.has({self.item.__str__().__repr__()}, p)"

  def __init__(self, item: I) -> None:
    self.item = item
    super().__init__()
