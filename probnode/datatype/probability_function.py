from typing import Callable, Union
import inspect


class ProbabilityFunction:

  def __init__(self, prob_function: Callable):
    self.probability_function = prob_function

  def __call__(self, *args):
    return self.probability_function(*args)

  def __repr__(self) -> str:
    return self.probability_function.__name__ + str(inspect.signature(self.probability_function))

  def __eq__(self, other: object) -> bool:
    if not callable(other):
      raise TypeError(
          f"Cannot compare {ProbabilityFunction.__name__} to non-callable {type(other).__name__}"
          )

    return False

  def __add__(self, other: "ProbabilityFunction") -> "ProbabilityFunction":

    def sum_f(*args):
      return self(*args) + other(*args)

    return ProbabilityFunction(sum_f)

  def __sub__(self, other: "ProbabilityFunction") -> "ProbabilityFunction":

    def subtract_f(*args):
      return self(*args) - other(*args)

    return ProbabilityFunction(subtract_f)

  def __mul__(self, other: "ProbabilityFunction") -> "ProbabilityFunction":

    def multiply_f(*args):
      return self(*args) * other(*args)

    return ProbabilityFunction(multiply_f)

  def __truediv__(self, other: "ProbabilityFunction") -> "ProbabilityFunction":

    def divide_f(*args):
      return self(*args) / other(*args)

    return ProbabilityFunction(divide_f)

  def __neg__(self) -> "ProbabilityFunction":

    def negative_f(*args):
      return 0 - self(*args)

    return ProbabilityFunction(negative_f)

  def __rsub__(self, other: Union[float, int]) -> "ProbabilityFunction":
    if not isinstance(other, (int, float)):
      raise TypeError(
          f"Cannot subtract {ProbabilityFunction.__name__} object from object of type {type(other)}"
          )

    def rsubstract_f(*args):
      return float(other) - self(*args)

    return ProbabilityFunction(rsubstract_f)

  def __radd__(self, other: Union[float, int]) -> "ProbabilityFunction":
    if not isinstance(other, (int, float)):
      raise TypeError(
          f"Cannot add {ProbabilityFunction.__name__} object with object of type {type(other)}"
          )

    def radd_f(*args):
      return float(other) + self(*args)

    return ProbabilityFunction(radd_f)

  def __rmul__(self, other: Union[float, int]) -> "ProbabilityFunction":
    if not isinstance(other, (int, float)):
      raise TypeError(
          f"Cannot multiply {ProbabilityFunction.__name__} object with object of type {type(other)}"
          )

    def rmul_f(*args):
      return float(other) * self(*args)

    return ProbabilityFunction(rmul_f)

  def __rtruediv__(self, other: Union[float, int]) -> "ProbabilityFunction":
    if not isinstance(other, (int, float)):
      raise TypeError(
          f"Cannot divide {ProbabilityFunction.__name__} object from object of type {type(other)}"
          )

    def rtruediv_f(*args):
      return float(other) / self(*args)

    return ProbabilityFunction(rtruediv_f)
