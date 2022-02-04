from proba.interface.iEvent import IEvent
from proba.probability import BaseProbabilityExpression, ProbabilityExpression


def P(expression):
  if isinstance(expression, IEvent):
    return ProbabilityExpression.from_event(expression)
  if isinstance(expression, BaseProbabilityExpression):
    return expression
