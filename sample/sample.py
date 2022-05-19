from probnode import Outcome, ES
from probnode.probability.event_set import GenericSureEventSet

outcome1 = Outcome("Outcome 1")
outcome1_event = ES(outcome1)
outcome2 = Outcome("Outcome 2")
outcome2_event = ES(outcome2)

outcome_1_or_2_event = ES(outcome1_event | outcome2_event)     # Or events
outcome_1_and_2_event = ES(outcome1_event & outcome2_event)     # And events
outcome_1_when_2_event = ES(outcome1_event // outcome2_event)     # Conditional event

# Display mathematical representation of the object(s)
print(repr(outcome1_event))

# Probability of events
from probnode import P

p_1 = P(outcome1_event)     # Each below is a probability measure
p_2 = P(outcome2_event)
p_1_or_2 = P(outcome_1_or_2_event)
p_1_and_2 = P(outcome_1_and_2_event)
p_1_when_2 = P(outcome_1_when_2_event)

# A sum of nodes
sum_p = 2.0 + p_1 + p_2 - 1 - p_1_and_2 + P(GenericSureEventSet())
# A product of nodes
product_p = p_1_when_2 * p_2

from probnode.computation import contract

contracted_sum_p = contract(sum_p)
print(repr(contracted_sum_p))
contracted_product_p = contract(product_p)
print(repr(contracted_product_p))

from probnode.computation import expand

x = expand(p_1_or_2)
print(repr(x[0]))
print(repr(sum_p))