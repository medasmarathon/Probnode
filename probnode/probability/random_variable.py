from typing import Any, Callable


class RandomVariable:
  def __init__(self, probability_function: Callable = lambda x: float(0)) -> None:
    self.probability_function = probability_function

  def __call__(self, *args: Any, **kwds: Any) -> Any:
    return self.probability_function(*args)