from typing import List, cast
from probnode.probability.probability_measure import ProbabilityMeasureOfEvent
from probnode.probability.event import GenericSureEvent
from probnode.probability.event import *
from probnode import *


def expand_and_apply_P_on_event(event: BaseEvent) -> List[ProbabilityMeasureOfEvent]:
  if type(event) is AtomicEvent:
    return [ProbabilityMeasureOfEvent(event)]
  if type(event) is ComplementaryAtomicEvent:
    return [
        ProbabilityMeasureOfEvent(GenericSureEvent()) -
        ProbabilityMeasureOfEvent(event.complement())
        ]
  if issubclass(type(event), ConditionalEvent):
    event = cast(ConditionalEvent, event)
    return [
        ProbabilityMeasureOfEvent(event.subject_event
                                  & event.condition_event) /
        ProbabilityMeasureOfEvent(event.condition_event)
        ]
  if issubclass(type(event), UnconditionalEvent):
    return expand_and_apply_P_on_unconditional_event(event)
  return [ProbabilityMeasureOfEvent(event)]


def expand_and_apply_P_on_unconditional_event(
    expression: UnconditionalEvent
    ) -> List[ProbabilityMeasureOfEvent]:
  if type(expression) is OrEvent:
    return [
        ProbabilityMeasureOfEvent(expression.base_event) +
        ProbabilityMeasureOfEvent(expression.aux_event) -
        ProbabilityMeasureOfEvent(expression.base_event & expression.aux_event)
        ]
  if type(expression) is AndEvent:
    return [
        ProbabilityMeasureOfEvent(expression.base_event // expression.aux_event) *
        ProbabilityMeasureOfEvent(expression.aux_event),
        ProbabilityMeasureOfEvent(expression.aux_event // expression.base_event) *
        ProbabilityMeasureOfEvent(expression.base_event)
        ]
