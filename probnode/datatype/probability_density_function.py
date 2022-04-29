from typing import Callable


class ProbabilityDensityFunction:

  def __init__(self, density_function: Callable[[float], float]):
    self.density_function = density_function

  def __call__(self, x: float) -> float:
    return self.density_function(x)