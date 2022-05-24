from typing import Any, Callable
from probnode.datatype.probability_function import ProbabilityFunction
from pyfields import field
from probnode.interface.ievent import IEvent
from probnode.probability.sample_space import SampleSpace


class RandomVariable:

  sample_space: SampleSpace = field(default=SampleSpace())
  probability_function: ProbabilityFunction = field(
      default=ProbabilityFunction(lambda event_set: None)
      )

  # Events cross interactions, eg. non-independent Events / Outcomes ?
  # Random Variable = f(x) * g(x) * h(x) | x is Event Set

  def __init__(
      self,
      probability_function: ProbabilityFunction = ProbabilityFunction(lambda event_set: None),
      sample_space: SampleSpace = SampleSpace()
      ) -> None:
    if not issubclass(type(probability_function), ProbabilityFunction):
      raise TypeError(
          f"Cannot assign {type(probability_function)} as {ProbabilityFunction.__name__}"
          )
    self.probability_function = probability_function
    self.sample_space = sample_space

  def __call__(self, event: IEvent = None, *args: Any, **kwds: Any) -> Any:
    if event is None or not event.get_outcome_set().issubset(self.sample_space.get_outcome_set()):
      return float(0)
    return self.probability_function(event)