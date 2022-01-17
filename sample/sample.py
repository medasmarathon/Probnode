from proba.event import Event
from proba.probability import BaseProbability, POperator
from proba.probabilityexpression import DenomFreeProbabilityExpression, ProbabilityExpression

e = Event()
p = ProbabilityExpression.from_event(POperator.DEFAULT, e)
e1 = Event()
p1 = ProbabilityExpression.from_event(POperator.DEFAULT, e1)
p2 = p1 + p
p3 = ProbabilityExpression.invert(p)
print(p2.base_node_tree == p1)
print(type(p3))
print(p3.base_node_tree)
print(p3.base_event)

print(p2.is_simple())
print(p3.is_base())