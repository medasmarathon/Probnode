from proba.event import Event
from proba.probability import POperator
from proba.probabilityexpression import DenomFreeProbabilityExpression, ProbabilityExpression

e = Event()
p = ProbabilityExpression(POperator.DEFAULT, e)
e1 = Event()
p1 = ProbabilityExpression(POperator.DEFAULT, e1)
p2 = p1 + p
p3 = ProbabilityExpression.invert(p)