from typing import Generic, TypeVar, override
from . import Logic

V = TypeVar("V")

class Option(Logic, Generic[V]):
  @override
  def __str__(self) -> str:
    return f"Option {self.option} = {self.value}"

  def __init__(self, option: str, value: V = True):
    super().__init__()
    self.option = option
    self.value = value

