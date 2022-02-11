from probnode.computation.expand import *
from probnode import Event
from probnode import P
from probnode import N

e = Event("Rain")
p = P(e)
e1 = Event("Hot")
p1 = P(e1)
e2 = Event("Es")
p6 = P(e2)
e3 = Event("Mn")
p7 = P(e3)
p2 = P(p1 | p)
p3 = p.invert()
p4 = P(p3 // p2)

p5 = p2.invert()
#p6 = p5.invert()
# print(repr(p2))
# n = expand(N(p2))
# print(repr(n))
# print(repr(p4))
# print(repr(p5))
# print(repr(p6))

print("\n")
chain = N(p2) + N(p6) - N(p6) * N(p7)
print(repr(chain))
ex_chain = expand(chain)
for item in ex_chain:
  print(f"\n {repr(item)}")
print("\n")

# print(repr(N(p3)))
# n = expand(N(p3))
# print(repr(n))

     #print(get_alternatives_from_list_of_possible_items([[1, 2], [3, 4], [5, 6, 7]]))
