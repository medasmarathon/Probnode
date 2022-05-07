from typing import List, cast
from probnode.core.node import Node
from probnode.probability.outcome import SureEvent
from probnode.probability.event import *
from probnode import *


def expand_probability_exp(expression: BaseEvent) -> List[Node]:
  if type(expression) is SimpleEvent:
    return [Node(expression)]
  if type(expression) is SimpleInvertEvent:
    return [Node(E(SureEvent())) - Node(expression.invert())]
  if issubclass(type(expression), ConditionalEvent):
    expression = cast(ConditionalEvent, expression)
    return [
        Node(E(expression.subject_event)
             & E(expression.condition_event)) / Node(E(expression.condition_event))
        ]
  if issubclass(type(expression), UnconditionalEvent):
    return expand_unconditional_exp(expression)
  return [Node(expression)]


def expand_unconditional_exp(expression: UnconditionalEvent) -> List[Node]:
  if type(expression) is OrEvent:
    return [
        Node(E(expression.base_event)) + Node(E(expression.aux_event)) -
        Node(E(expression.base_event) & E(expression.aux_event))
        ]
  if type(expression) is AndEvent:
    return [
        Node(E(expression.base_event // expression.aux_event)) * Node(E(expression.aux_event)),
        Node(E(expression.aux_event // expression.base_event)) * Node(E(expression.base_event))
        ]
