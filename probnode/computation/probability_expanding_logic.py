from typing import List
from probnode.core.node import Node
from probnode.probability.event import SureEvent
from probnode.probability.probability import *
from probnode import *


def expand_probability_exp(expression: BaseProbabilityExpression) -> List[Node]:
  if type(expression) is SimpleProbabilityExpression:
    return [Node(expression)]
  if type(expression) is SimpleInvertProbabilityExpression:
    return [Node(P(SureEvent())) - Node(expression.invert())]
  if issubclass(type(expression), ConditionalProbabilityExpression):
    return [
        Node(P(expression.subject_exp)
             & P(expression.condition_exp)) / Node(P(expression.condition_exp))
        ]
  if issubclass(type(expression), UnconditionalProbabilityExpression):
    return expand_unconditional_exp(expression)
  return [Node(expression)]


def expand_unconditional_exp(expression: UnconditionalProbabilityExpression) -> List[Node]:
  if type(expression) is OrProbabilityExpression:
    return [
        Node(P(expression.base_exp)) + Node(P(expression.aux_exp)) -
        Node(P(expression.base_exp) & P(expression.aux_exp))
        ]
  if type(expression) is AndProbabilityExpression:
    return [
        Node(P(expression.base_exp // expression.aux_exp)) * Node(P(expression.aux_exp)),
        Node(P(expression.aux_exp // expression.base_exp)) * Node(P(expression.base_exp))
        ]
