from typing import List, cast
from probnode.probability.probability_measure import ProbabilityMeasure
from probnode.probability.event_set import GenericSureEventSet
from probnode.probability.event_set import *
from probnode import *


def expand_probability_exp(expression: BaseEventSet) -> List[ProbabilityMeasure]:
  if type(expression) is SimpleEventSet:
    return [ProbabilityMeasure(expression)]
  if type(expression) is SimpleInvertEventSet:
    return [
        ProbabilityMeasure(ES__(GenericSureEventSet())) - ProbabilityMeasure(expression.invert())
        ]
  if issubclass(type(expression), ConditionalEventSet):
    expression = cast(ConditionalEventSet, expression)
    return [
        ProbabilityMeasure(ES__(expression.subject_event)
                           & ES__(expression.condition_event)) /
        ProbabilityMeasure(ES__(expression.condition_event))
        ]
  if issubclass(type(expression), UnconditionalEventSet):
    return expand_unconditional_exp(expression)
  return [ProbabilityMeasure(expression)]


def expand_unconditional_exp(expression: UnconditionalEventSet) -> List[ProbabilityMeasure]:
  if type(expression) is OrEventSet:
    return [
        ProbabilityMeasure(ES__(expression.base_event)) +
        ProbabilityMeasure(ES__(expression.aux_event)) -
        ProbabilityMeasure(ES__(expression.base_event) & ES__(expression.aux_event))
        ]
  if type(expression) is AndEventSet:
    return [
        ProbabilityMeasure(ES__(expression.base_event // expression.aux_event)) *
        ProbabilityMeasure(ES__(expression.aux_event)),
        ProbabilityMeasure(ES__(expression.aux_event // expression.base_event)) *
        ProbabilityMeasure(ES__(expression.base_event))
        ]
