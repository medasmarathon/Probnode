from proba.computation.chain import Node
from proba.computation.expand import expand
from proba.event import Event
from proba.utilities.P import P

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
print(repr(expand(Node(p2))))
# print(repr(p4))
# print(repr(p5))
# print(repr(p6))

# chain = Node(p5) + Node(p) - Node(p1) * Node(p3)
# print(repr(chain))

print(repr(Node(p3)))
n = expand(Node(p3))
print(repr(n))
