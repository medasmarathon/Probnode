from typing import Any, Callable

from probnode.interface.ievent import IEvent


class RandomVariable:

  def __init__(self, probability_function: Callable = lambda event_set: float(0)) -> None:
    self.probability_function = probability_function

  def __call__(self, event_set: IEvent = None, *args: Any, **kwds: Any) -> Any:
    if event_set is None:
      return float(0)
    return self.probability_function(event_set)