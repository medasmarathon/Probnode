from typing import Callable, Union
from probnode.datatype.probability_distribution_function import ProbabilityDistributionFunction
from probnode.datatype.probability_value import ProbabilityValue
from pyfields import field


class IProbability:
  _value: Union[ProbabilityDistributionFunction, ProbabilityValue] = field(default=None)

  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, value):
    if callable(value):
      self._value = ProbabilityDistributionFunction(value)
    else:
      self._value = value
