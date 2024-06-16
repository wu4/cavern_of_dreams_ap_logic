from typing import TypeAlias

from .objects import InternalEvent
from .has import Collected as _Collected
from ..generated_types import eventItem, teleportItem

HasEventType: TypeAlias = eventItem | teleportItem | type[InternalEvent]

class Collected(_Collected[HasEventType]):
  pass
