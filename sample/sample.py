from proba.event import Event
from proba.interface.iProbabilityExpression import PMathNotation
from proba.probability import POperator
from proba.probabilityexpression import ProbabilityExpression
from proba.strategy.probabilityExpressionChain import ProbabilityExpressionChain
from proba.utilities.P import P

e = Event("Rain")
p = P(e)
e1 = Event("Hot")
p1 = P(e1)
p2 = p1 + p
p3 = p.invert()
p4 = p3 // p2

chain = ProbabilityExpressionChain()
chain.with_prob_exp(p2).do(PMathNotation.ADD).with_prob_exp(p3)
print(repr(chain))