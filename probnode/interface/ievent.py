from typing import Callable, Set, Union
from probnode.datatype.probability_value import ProbabilityValue
from pyfields import field


class IEvent:

  def get_outcome_set(self) -> Set:
    raise NotImplementedError
