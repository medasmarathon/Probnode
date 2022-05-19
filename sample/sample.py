from probnode import Outcome, E
from probnode.probability.outcome import SureEvent

outcome1 = Outcome("Sample event 1")
outcome1_event = E(outcome1)
outcome2 = Outcome("Sample event 2")
outcome2_event = E(outcome2)

outcome_1_or_2_event = E(outcome1_event | outcome2_event)     # Or Probability expression
outcome_1_and_2_event = E(outcome1_event & outcome2_event)     # And Probability expression
outcome_1_when_2_event = E(
    outcome1_event // outcome2_event
    )     # Conditional Probability expression

# Display mathematical representation of the object(s)
print(repr(outcome1_event))

# First convert probability expression to math node
from probnode import N

n1 = N(outcome1_event)     # Each below is a (math) node
n2 = N(outcome2_event)
n_1_or_2 = N(outcome_1_or_2_event)
n_1_and_2 = N(outcome_1_and_2_event)
n_1_when_2 = N(outcome_1_when_2_event)

# A sum of nodes
snode = 2.0 + n1 + n2 - 1 - n_1_and_2 + N(E(SureEvent()))
# A product of nodes
pnode = n_1_when_2 * n2

from probnode.computation import contract

c1 = contract(snode)
print(repr(c1))
c2 = contract(pnode)
print(repr(c2))

from probnode.computation import expand

x = expand(n_1_or_2)
print(repr(x[0]))
print(repr(snode))