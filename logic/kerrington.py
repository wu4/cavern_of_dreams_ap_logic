from typing import Literal, TypeAlias, override
from .logic import Logic, Not

TiltType: TypeAlias = Literal[-1, 0, 1]

class Tilt(Logic):
  def __init__(self, tilt: TiltType):
    self.tilt = tilt
    super().__init__()

  @override
  def __str__(self) -> str:
    return f"Kerrington Tilt ({self.tilt})"

  @override
  def into_server_code(self) -> str:
    return f"s._cavernofdreams_kerrington_tilt[p]=={self.tilt}"

no_tilt = Tilt(0)
any_tilt = Not(no_tilt)
left_tilt = Tilt(-1)
right_tilt = Tilt(1)
