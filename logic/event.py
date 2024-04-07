from typing import TypeAlias
from ..generated import eventItem, teleportItem
from .objects import InternalEvent
from . import Logic

HasEventType: TypeAlias = eventItem | teleportItem | type[InternalEvent]

class HasEvent(Logic):
  def __str__(self) -> str:
    return f"Has {self.has}"
  
  def __init__(self, has: HasEventType) -> None:
    self.has = has
    super().__init__()