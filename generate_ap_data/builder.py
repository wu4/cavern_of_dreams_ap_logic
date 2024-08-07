from abc import abstractmethod
from typing import TYPE_CHECKING

from ..logic.carrying import Carrying
from ..logic.logic import All, Logic
from ..logic_parsing.options import OptionKey, distribute_logic_by_options


if TYPE_CHECKING:
  from ..logic.logic import MaybeLogic
  from ..logic_parsing.carryables import CarryableKey


class Builder:
  lines: list[str]
  indent: int

  def __init__(self):
    super().__init__()
    self.lines = []
    self.indent = 0

  def add_line(self, line: str):
    self.lines.append(("  " * self.indent) + line)

  @abstractmethod
  def run(self): ...

  @classmethod
  def build(cls) -> str:
    a = cls()
    a.run()
    return "\n".join(a.lines)

  def define_dict(self, var_name: str, dictionary: dict[str, str]):
    self.add_line(f"{var_name}="+'{')
    self.indent += 1
    for k, v in dictionary.items():
      self.add_line(f"{k}:{v},")
    self.indent -= 1
    self.add_line("}")

  def define_rules(self, rule: "MaybeLogic", var_name: str):
    if rule is None:
      self.add_line(f"{var_name}.dont_care_access_rule=lambda s:True")
      return

    from ..logic_parsing.carryables import distribute_carryable_logic
    from ..logic_parsing.helpers import simplify, nested_list_to_logic
    from ..logic.logic import Not

    distributed = distribute_carryable_logic(rule)

    def full_logic(case: "CarryableKey"):
      all_logic = distributed[case]
      if all_logic == []:
        return "lambda s:True"

      string_builder = "construct_rule(p,("

      def sort_by_branch_size(logic: "tuple[OptionKey, list[list[Logic]]]"):
        return sum(map(len, logic[1]))

      by_options = sorted(distribute_logic_by_options(nested_list_to_logic(all_logic)), key=sort_by_branch_size)
      for options, logics in by_options:
        if options == "dont-care":
          test = "True"
        else:
          test = All(*options).into_server_code()

        if logics == []:
          logic_str = "True"
        else:
          logic_str = simplify(logics).into_server_code()

        string_builder += f"({test}, {repr(logic_str)}),"
      string_builder += "))"
      return string_builder

    inverse_rules: dict[str, str] = {}
    rules: dict[str, str] = {}

    for case in distributed:
      # handle this below
      if case == "dont-care": continue

      case_rule = full_logic(case)
      # case_rule = simplified_logic(case)
      if isinstance(case, Not):
        assert isinstance(case.logic, Carrying)
        inverse_rules[repr(case.logic.carryable)] = case_rule
      else:
        rules[repr(case.carryable)] = case_rule

    if "dont-care" in distributed:
      dont_care_rule = full_logic('dont-care')
      # dont_care_rule = simplified_logic('dont-care')
      self.add_line(f"{var_name}.dont_care_access_rule={dont_care_rule}")

    self.define_dict(f"{var_name}.inverse_carryable_access_rules", inverse_rules)
    self.define_dict(f"{var_name}.carryable_access_rules", rules)

