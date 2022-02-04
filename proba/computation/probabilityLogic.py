from platform import node
from proba.computation.chain import Node, ProductNode
from proba.event import SureEvent
from proba.probability import AndProbabilityExpression, BaseProbabilityExpression, ConditionalProbabilityExpression, SimpleInvertProbabilityExpression, SimpleProbabilityExpression, UnconditionalProbabilityExpression


def expand_probability_exp(expression: BaseProbabilityExpression) -> Node:
  if type(expression) is SimpleProbabilityExpression:
    return Node(expression)
  if type(expression) is SimpleInvertProbabilityExpression:
    return Node(BaseProbabilityExpression.from_event(SureEvent())) - Node(expression.invert())
  if issubclass(expression, ConditionalProbabilityExpression):
    pass
  elif issubclass(expression, UnconditionalProbabilityExpression):
    pass
  node = Node()
  return node
