from typing import Union


class ProbabilityValue(float):

  def __new__(cls, value: Union[bool, float]):
    if type(value) is bool:
      return super().__new__(cls, int(value))

    if value < 0:
      raise ValueError("probability must not be less than 0")
    if value > 1:
      raise ValueError("probability must not be greater than 1")
    return super().__new__(cls, value)

  def __add__(self, other: float):
    res = super(ProbabilityValue, self).__add__(other)
    return self.__class__(min(1, max(res, 0)))

  def __sub__(self, other: float):
    res = super(ProbabilityValue, self).__sub__(other)
    return self.__class__(min(1, max(res, 0)))

  def __mul__(self, other: float):
    res = super(ProbabilityValue, self).__mul__(other)
    return self.__class__(min(1, max(res, 0)))

  def __truediv__(self, other: float):
    res = super(ProbabilityValue, self).__truediv__(other)
    return self.__class__(min(1, max(res, 0)))