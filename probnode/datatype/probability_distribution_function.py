from typing import Callable


class ProbabilityDistributionFunction:

  def __init__(self, distribution_function: Callable):
    self.distribution_function = distribution_function

  def __call__(self, *args):
    return self.distribution_function(*args)

  def __eq__(self, other: object) -> bool:
    if not callable(other):
      raise TypeError(
          f"Cannot compare {ProbabilityDistributionFunction.__name__} to non-callable {type(other).__name__}"
          )

    return False

  def __add__(self, other: "ProbabilityDistributionFunction") -> "ProbabilityDistributionFunction":

    def sum_f(*args):
      return self(*args) + other(*args)

    return ProbabilityDistributionFunction(sum_f)

  def __sub__(self, other: "ProbabilityDistributionFunction") -> "ProbabilityDistributionFunction":

    def subtract_f(*args):
      return self(*args) - other(*args)

    return ProbabilityDistributionFunction(subtract_f)

  def __mul__(self, other: "ProbabilityDistributionFunction") -> "ProbabilityDistributionFunction":

    def multiply_f(*args):
      return self(*args) * other(*args)

    return ProbabilityDistributionFunction(multiply_f)

  def __truediv__(
      self, other: "ProbabilityDistributionFunction"
      ) -> "ProbabilityDistributionFunction":

    def divide_f(*args):
      return self(*args) / other(*args)

    return ProbabilityDistributionFunction(divide_f)

  def __neg__(self) -> "ProbabilityDistributionFunction":

    def negative_f(*args):
      return 0 - self(*args)

    return negative_f