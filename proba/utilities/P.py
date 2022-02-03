from proba.event import Event
from proba.probability import BaseProbabilityExpression, ProbabilityExpression


def P(expression):
  if isinstance(expression, Event):
    return ProbabilityExpression.from_event(expression)
  if isinstance(expression, BaseProbabilityExpression):
    return expression
