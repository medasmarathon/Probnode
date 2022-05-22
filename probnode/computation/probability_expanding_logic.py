from typing import List, cast
from probnode.probability.probability_measure import ProbabilityMeasure
from probnode.probability.event_set import GenericSureEvent
from probnode.probability.event_set import *
from probnode import *


def expand_probability_exp(expression: BaseEvent) -> List[ProbabilityMeasure]:
  if type(expression) is AtomicEvent:
    return [ProbabilityMeasure(expression)]
  if type(expression) is ComplementaryAtomicEvent:
    return [
        ProbabilityMeasure(Event(GenericSureEvent())) - ProbabilityMeasure(expression.complement())
        ]
  if issubclass(type(expression), ConditionalEvent):
    expression = cast(ConditionalEvent, expression)
    return [
        ProbabilityMeasure(Event(expression.subject_event)
                           & Event(expression.condition_event)) /
        ProbabilityMeasure(Event(expression.condition_event))
        ]
  if issubclass(type(expression), UnconditionalEvent):
    return expand_unconditional_exp(expression)
  return [ProbabilityMeasure(expression)]


def expand_unconditional_exp(expression: UnconditionalEvent) -> List[ProbabilityMeasure]:
  if type(expression) is OrEvent:
    return [
        ProbabilityMeasure(Event(expression.base_event)) +
        ProbabilityMeasure(Event(expression.aux_event)) -
        ProbabilityMeasure(Event(expression.base_event) & Event(expression.aux_event))
        ]
  if type(expression) is AndEvent:
    return [
        ProbabilityMeasure(Event(expression.base_event // expression.aux_event)) *
        ProbabilityMeasure(Event(expression.aux_event)),
        ProbabilityMeasure(Event(expression.aux_event // expression.base_event)) *
        ProbabilityMeasure(Event(expression.base_event))
        ]
