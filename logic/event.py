from typing import TypeAlias

from . import Logic
from .objects import InternalEvent
from ..generated import eventItem, teleportItem

HasEventType: TypeAlias = eventItem | teleportItem | type[InternalEvent]

class Collected(Logic):
  def __str__(self) -> str:
    return f"Has {self.event}"
  
  def __init__(self, event: HasEventType) -> None:
    self.event = event
    super().__init__()