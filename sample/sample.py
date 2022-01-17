from proba.event import Event
from proba.probability import POperator
from proba.probabilityexpression import ProbabilityExpression

e = Event("Rain")
p = ProbabilityExpression.from_event(POperator.DEFAULT, e)
e1 = Event("Hot")
p1 = ProbabilityExpression.from_event(POperator.DEFAULT, e1)
p2 = p1 + p
p3 = p.invert()
p4 = p3 // p2

print(p2.is_simple())
print(p3.is_simple())
print(repr(p2))
print(repr(p3))
print(repr(p))
print(repr(p4))
