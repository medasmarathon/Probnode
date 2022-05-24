from typing import Callable, Set, Union
from pyfields import field


class IEvent:

  def get_outcome_set(self) -> Set:
    raise NotImplementedError
