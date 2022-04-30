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