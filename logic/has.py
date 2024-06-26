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

  "Jester Boots"
]

CollectedItem: TypeAlias = AnyItem | type[InternalEvent] | CarryingItem
I = TypeVar("I", bound=CollectedItem)

class Collected(Logic, Generic[I]):
  item: I

  @override
  def __str__(self) -> str:
    return f"Has {self.item}"

  @override
  def into_server_code(self) -> str:
    return f"s.has({str(self.item).__repr__()}, p)"

  def __init__(self, item: I) -> None:
    self.item = item
    super().__init__()


CollectedAny: TypeAlias = Collected[CollectedItem]
