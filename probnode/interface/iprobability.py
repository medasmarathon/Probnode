from typing import Callable, Union
from probnode.datatype.probability_density_function import ProbabilityDensityFunction
from probnode.datatype.probability_value import ProbabilityValue
from pyfields import field


class IProbability:
  _value: Union[ProbabilityDensityFunction, ProbabilityValue] = field(default=None)

  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, value):
    if callable(value):
      self._value = ProbabilityDensityFunction(value)
    else:
      self._value = value
