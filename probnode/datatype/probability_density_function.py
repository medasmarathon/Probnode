from typing import Callable


class ProbabilityDensityFunction:

  def __init__(self, density_function: Callable[[float], float]):
    self.density_function = density_function

  def __call__(self, x: float) -> float:
    return self.density_function(x)

  def __eq__(self, other: object) -> bool:
    if not callable(other):
      raise TypeError(
          f"Cannot compare {ProbabilityDensityFunction.__name__} to non-callable {type(other).__name__}"
          )

    return False

  def __add__(self, other: "ProbabilityDensityFunction") -> "ProbabilityDensityFunction":

    def sum_f(x: float) -> float:
      return self(x) + other(x)

    return ProbabilityDensityFunction(sum_f)

  def __sub__(self, other: "ProbabilityDensityFunction") -> "ProbabilityDensityFunction":

    def subtract_f(x: float) -> float:
      return self(x) - other(x)

    return ProbabilityDensityFunction(subtract_f)

  def __mul__(self, other: "ProbabilityDensityFunction") -> "ProbabilityDensityFunction":

    def multiply_f(x: float) -> float:
      return self(x) * other(x)

    return ProbabilityDensityFunction(multiply_f)

  def __truediv__(self, other: "ProbabilityDensityFunction") -> "ProbabilityDensityFunction":

    def divide_f(x: float) -> float:
      return self(x) / other(x)

    return ProbabilityDensityFunction(divide_f)

  def __neg__(self) -> "ProbabilityDensityFunction":

    def negative_f(x: float) -> float:
      return 0 - self(x)

    return negative_f