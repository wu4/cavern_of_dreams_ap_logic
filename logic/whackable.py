from .logic import Logic

class Whackable(Logic):
  def __init__(
    self,
    ground_tail_works: bool = False,
    air_tail_works: bool = False,
    roll_works: bool = False,
    throwable_works: bool = False,
    horn_works: bool = False
  ):
    super().__init__()
    self.ground_tail_works = ground_tail_works
    self.air_tail_works = air_tail_works
    self.roll_works = roll_works
    self.throwable_works = throwable_works
    self.horn_works = horn_works
