from probnode import Event, P
from probnode.probability.event import SureEvent

e1 = Event("Sample event 1")
p1 = P(e1)
e2 = Event("Sample event 2")
p2 = P(e2)

p3 = P(p1 | p2)     # Or Probability expression
p4 = P(p1 & p2)     # And Probability expression
p5 = P(p1 // p2)     # Conditional Probability expression

# Display mathematical representation of the object(s)
print(repr(p1))

# First convert probability expression to math node
from probnode import N

n1 = N(p1)     # Each below is a (math) node
n2 = N(p2)
n3 = N(p3)
n4 = N(p4)
n5 = N(p5)

# A sum of nodes
snode = 2.0 + n1 + n2 - 1 - n4 + N(P(SureEvent()))
# A product of nodes
pnode = n5 * n2

from probnode.computation import contract

c1 = snode.reduce(contract)
print(repr(c1))
c2 = contract(pnode)
print(repr(c2))

from probnode.computation import expand

x = expand(n3)
print(repr(x[0]))
print(repr(snode))