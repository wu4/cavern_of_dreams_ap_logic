from __future__ import annotations
from typing import TYPE_CHECKING, Generic, Literal, TypeAlias, override, TypeVar


from ..generated_types import AnyItem
if TYPE_CHECKING:
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

CollectedItem: TypeAlias = AnyItem | type["InternalEvent"] | CarryingItem
I = TypeVar("I", bound=CollectedItem)

class Collected(Logic, Generic[I]):
  item: I

  @override
  def __eq__(self, other) -> bool:
    if isinstance(other, Collected):
      return self.item == other.item
    return super().__eq__(other)

  @override
  def __hash__(self) -> int:
    return hash(self.item)

  @override
  def __str__(self) -> str:
    return f"Has {self.item}"

  @override
  def into_server_code(self) -> str:
    return f"s.has({repr(str(self.item))}, p)"

  def __init__(self, item: I) -> None:
    self.item = item
    super().__init__()

CollectedAny: TypeAlias = Collected[CollectedItem]
