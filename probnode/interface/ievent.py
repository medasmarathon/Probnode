from typing import Callable, Union
from probnode.datatype.probability_value import ProbabilityValue
from pyfields import field


class IEvent:
  pass
  # _value: Union[None, ProbabilityValue] = field(default=None)

  # @property
  # def value(self):
  #   return self._value

  # @value.setter
  # def value(self, value):
  #   self._value = value
