from typing import Callable, Optional, Union
import inspect
from functools import wraps


class ProbabilityDistribution:

  def __init__(self, prob_function: Callable):

    @wraps(prob_function)
    def wrapper(*args):
      prob = prob_function(*args)
      return prob if prob is not None else None

    self.probability_function = wrapper

  def __call__(self, *args):
    return self.probability_function(*args)

  def __repr__(self) -> str:
    return self.probability_function.__name__ + str(inspect.signature(self.probability_function))

  def __eq__(self, other: object) -> bool:
    if not callable(other):
      raise TypeError(
          f"Cannot compare {ProbabilityDistribution.__name__} to non-callable {type(other).__name__}"
          )

    return False

  def __add__(self, other: "ProbabilityDistribution") -> "ProbabilityDistribution":

    def sum_f(event) -> Optional[float]:
      self_prob = self(event)
      other_prob = other(event)
      return None if None in [self_prob, other_prob] else self_prob + other_prob

    sum_f.__name__ = f"(\U00002131:{self.probability_function.__name__} + \U00002131:{other.probability_function.__name__})"
    return ProbabilityDistribution(sum_f)

  def __sub__(self, other: "ProbabilityDistribution") -> "ProbabilityDistribution":

    def subtract_f(event) -> Optional[float]:
      self_prob = self(event)
      other_prob = other(event)
      return None if None in [self_prob, other_prob] else self_prob - other_prob

    subtract_f.__name__ = f"(\U00002131:{self.probability_function.__name__} - \U00002131:{other.probability_function.__name__})"
    return ProbabilityDistribution(subtract_f)

  def __mul__(self, other: "ProbabilityDistribution") -> "ProbabilityDistribution":

    def multiply_f(event) -> Optional[float]:
      self_prob = self(event)
      other_prob = other(event)
      return None if None in [self_prob, other_prob] else self_prob * other_prob

    multiply_f.__name__ = f"(\U00002131:{self.probability_function.__name__} * \U00002131:{other.probability_function.__name__})"

    return ProbabilityDistribution(multiply_f)

  def __truediv__(self, other: "ProbabilityDistribution") -> "ProbabilityDistribution":

    def divide_f(event) -> Optional[float]:
      self_prob = self(event)
      other_prob = other(event)
      return None if None in [self_prob, other_prob] else self_prob / other_prob

    divide_f.__name__ = f"(\U00002131:{self.probability_function.__name__} / \U00002131:{other.probability_function.__name__})"
    return ProbabilityDistribution(divide_f)

  def __neg__(self) -> "ProbabilityDistribution":

    def negative_f(event) -> Optional[float]:
      self_prob = self(event)
      return None if self_prob is None else 0 - self_prob

    negative_f.__name__ = f"-(\U00002131:{self.probability_function.__name__})"
    return ProbabilityDistribution(negative_f)

  def __rsub__(self, other: Union[float, int]) -> "ProbabilityDistribution":
    if not isinstance(other, (int, float)):
      raise TypeError(
          f"Cannot subtract {ProbabilityDistribution.__name__} object from object of type {type(other)}"
          )

    def rsubstract_f(event) -> Optional[float]:
      self_prob = self(event)
      return None if self_prob is None else float(other) - self_prob

    rsubstract_f.__name__ = f"{other} - (\U00002131:{self.probability_function.__name__})"
    return ProbabilityDistribution(rsubstract_f)

  def __radd__(self, other: Union[float, int]) -> "ProbabilityDistribution":
    if not isinstance(other, (int, float)):
      raise TypeError(
          f"Cannot add {ProbabilityDistribution.__name__} object with object of type {type(other)}"
          )

    def radd_f(event) -> Optional[float]:
      self_prob = self(event)
      return None if self_prob is None else float(other) + self_prob

    radd_f.__name__ = f"{other} + (\U00002131:{self.probability_function.__name__})"
    return ProbabilityDistribution(radd_f)

  def __rmul__(self, other: Union[float, int]) -> "ProbabilityDistribution":
    if not isinstance(other, (int, float)):
      raise TypeError(
          f"Cannot multiply {ProbabilityDistribution.__name__} object with object of type {type(other)}"
          )

    def rmul_f(event) -> Optional[float]:
      self_prob = self(event)
      return None if self_prob is None else float(other) * self_prob

    rmul_f.__name__ = f"{other} * (\U00002131:{self.probability_function.__name__})"
    return ProbabilityDistribution(rmul_f)

  def __rtruediv__(self, other: Union[float, int]) -> "ProbabilityDistribution":
    if not isinstance(other, (int, float)):
      raise TypeError(
          f"Cannot divide {ProbabilityDistribution.__name__} object from object of type {type(other)}"
          )

    def rtruediv_f(event) -> Optional[float]:
      self_prob = self(event)
      return None if self_prob is None else float(other) / self_prob

    rtruediv_f.__name__ = f"{other} / (\U00002131:{self.probability_function.__name__})"
    return ProbabilityDistribution(rtruediv_f)
