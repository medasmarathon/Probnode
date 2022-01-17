from proba.event import Event
from proba.probability import BaseProbabilityExpression, POperator
from proba.probabilityexpression import ProbabilityExpression


def P(expression):
  if isinstance(expression, Event):
    return ProbabilityExpression.from_event(POperator.DEFAULT, expression)
  if isinstance(expression, BaseProbabilityExpression):
    return expression
