from typing import override

from .logic import Logic

class HasQuantity(Logic):
  def __init__(self, group_name: str, amount: int) -> None:
    self.group_name = group_name
    self.amount = amount
    super().__init__()

  @override
  def into_server_code(self) -> str:
    return f"s.has_group({self.group_name.__repr__()}, p, {self.amount})"

class HasEggs(HasQuantity):
  def __init__(self, amount: int) -> None:
    super().__init__("Egg", amount)

  @override
  def __str__(self) -> str:
    return f"Has at least {self.amount} eggs"

class AllEggs(Logic):
  @override
  def __str__(self) -> str:
    return f"Has all eggs"

  @override
  def into_server_code(self) -> str:
    return f"s.has_all(all_eggs,p)"

class HasGratitude(HasQuantity):
  def __init__(self, amount: int) -> None:
    super().__init__("Gratitude", amount)

  @override
  def __str__(self) -> str:
    return f"Has at least {self.amount} gratitude"

class HasShrooms(Logic):
  @override
  def __str__(self) -> str:
    return f"Has enough shrooms for the {self.shroom_count_source} fella"

  def __init__(self, shroom_count_source: str):
    super().__init__()
    self.shroom_count_source = shroom_count_source

  @override
  def into_server_code(self) -> str:
    return f"s._cavernofdreams_has_shrooms_for(p,{repr(self.shroom_count_source)})"
