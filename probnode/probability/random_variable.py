from typing import Any, Callable
from probability_distribution import ProbabilityDistribution
from pyfields import field
from probnode.interface.ievent import IEvent
from probnode.probability.sample_space import SampleSpace


class RandomVariable:

  sample_space: SampleSpace = field(default=None)
  probability_function: ProbabilityDistribution = field(
      default=ProbabilityDistribution(lambda event_set: None)
      )

  # Events cross interactions, eg. non-independent Events / Outcomes ?
  # Random Variable = f(x) * g(x) * h(x) | x is Event Set

  def __init__(
      self,
      probability_function: ProbabilityDistribution = ProbabilityDistribution(
          lambda event_set: None
          ),
      sample_space: SampleSpace = None
      ) -> None:
    if not issubclass(type(probability_function), ProbabilityDistribution):
      raise TypeError(
          f"Cannot assign {type(probability_function)} as {ProbabilityDistribution.__name__}"
          )
    self.probability_function = probability_function
    self.sample_space = sample_space

  def __call__(self, event: IEvent = None, *args: Any, **kwds: Any) -> Any:
    if event is None or (self.sample_space is not None and
                         not event.get_outcome_set().issubset(self.sample_space.get_outcome_set())):
      return None
    return self.probability_function(event)

  def __repr__(self) -> str:
    return f"\U00002131 = {repr(self.probability_function)}: {repr(self.sample_space)} -> [0,1]"