from typing import Any, Callable
from probnode.datatype.probability_function import ProbabilityFunction
from pyfields import field
from probnode.interface.ievent import IEvent
from probnode.probability.sample_space import SampleSpace


class RandomVariable:

  sample_space: SampleSpace = field(default=SampleSpace())

  # Event Space ?
  # Event Sets cross interactions, eg. non-independent Event Sets / Outcomes ?
  # Random Variable = f(x) * g(x) * h(x) | x is Event Set

  def __init__(
      self, probability_function: ProbabilityFunction = ProbabilityFunction(lambda event_set: None)
      ) -> None:
    if not issubclass(type(probability_function), ProbabilityFunction):
      raise TypeError(
          f"Cannot assign {type(probability_function)} as {ProbabilityFunction.__name__}"
          )
    self.probability_function = probability_function

  def __call__(self, event: IEvent = None, *args: Any, **kwds: Any) -> Any:
    if event is None:
      return float(0)
    return self.probability_function(event)