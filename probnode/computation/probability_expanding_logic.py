from typing import List, cast
from probnode.probability.probability_measure import ProbabilityMeasure
from probnode.probability.event import GenericSureEvent
from probnode.probability.event import *
from probnode import *


def expand_and_apply_P_on_event(event: BaseEvent) -> List[ProbabilityMeasure]:
  if type(event) is AtomicEvent:
    return [ProbabilityMeasure(event)]
  if type(event) is ComplementaryAtomicEvent:
    return [ProbabilityMeasure(Event(GenericSureEvent())) - ProbabilityMeasure(event.complement())]
  if issubclass(type(event), ConditionalEvent):
    event = cast(ConditionalEvent, event)
    return [
        ProbabilityMeasure(Event(event.subject_event)
                           & Event(event.condition_event)) /
        ProbabilityMeasure(Event(event.condition_event))
        ]
  if issubclass(type(event), UnconditionalEvent):
    return expand_and_apply_P_on_unconditional_event(event)
  return [ProbabilityMeasure(event)]


def expand_and_apply_P_on_unconditional_event(
    expression: UnconditionalEvent
    ) -> List[ProbabilityMeasure]:
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
