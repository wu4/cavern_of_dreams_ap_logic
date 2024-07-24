from typing import Generic, TypeAlias, TypeVar, override, Any as AnyType

from .logic import Logic

V = TypeVar("V")

class Option(Logic, Generic[V]):
  @override
  def __hash__(self) -> int:
    return hash((self.option, self.value, self.greater_or_equal))

  @override
  def __str__(self) -> str:
    return f"Option {self.option} = {self.value}"

  @override
  def __eq__(self, other: object, /) -> bool:
    if isinstance(other, Option):
      return self.option == other.option and self.value == other.value and self.greater_or_equal == other.greater_or_equal
    return super().__eq__(other)

  def __init__(self, option: str, value: V = 1, greater_or_equal: bool = False):
    super().__init__()
    self.option = option
    self.value = value
    self.greater_or_equal = greater_or_equal

  @override
  def into_server_code(self) -> str:
    eq_str = ">=" if self.greater_or_equal else "=="
    # return f"s.multiworld.worlds[p].options.{self.option}.value {eq_str} {self.value.__repr__()}"
    return f"o.{self.option}.value {eq_str} {self.value.__repr__()}"

AnyOption: TypeAlias = Option[AnyType]
