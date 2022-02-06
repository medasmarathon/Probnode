from proba.computation.expand import expand
from proba import Event
from proba import P
from proba import N

e = Event("Rain")
p = P(e)
e1 = Event("Hot")
p1 = P(e1)
p2 = P(p1 | p)
p3 = p.invert()
p4 = P(p3 // p2)

p5 = p2.invert()
p6 = p5.invert()
print(repr(p2))
n = expand(N(p2))
print(repr(n))
print(repr(p4))
print(repr(p5))
print(repr(p6))

print("\n")
chain = N(p5) + N(p) - N(p1) * N(p3)
print(repr(chain))
ex_chain = expand(chain)
print(repr(ex_chain))
print("\n")

print(repr(N(p3)))
n = expand(N(p3))
print(repr(n))
