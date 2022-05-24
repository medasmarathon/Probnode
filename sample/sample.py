from probnode import Outcome, Event, P__
from probnode.datatype.probability_function import ProbabilityFunction
from probnode.probability.event import BaseEvent, GenericSureEvent
from probnode.probability.random_variable import RandomVariable
from probnode.probability.sample_space import SampleSpace

outcome1 = Outcome("Outcome 1")
outcome1_event = Event(outcome1)
outcome2 = Outcome("Outcome 2")
outcome2_event = Event(outcome2)

outcome_1_or_2_event = Event(outcome1_event | outcome2_event)     # Or events
outcome_1_and_2_event = Event(outcome1_event & outcome2_event)     # And events
outcome_1_when_2_event = Event(outcome1_event // outcome2_event)     # Conditional event

# Display mathematical representation of the object(s)
print(repr(outcome1_event))

# Probability of events
from probnode import p__X_

p_1 = p__X_(outcome1_event)     # Each below is a probability measure
p_2 = p__X_(outcome2_event)
p_1_or_2 = p__X_(outcome_1_or_2_event)
p_1_and_2 = p__X_(outcome_1_and_2_event)
p_1_when_2 = p__X_(outcome_1_when_2_event)

# A sum of nodes
sum_p = 2.0 + p_1 + p_2 - 1 - p_1_and_2 + p__X_(GenericSureEvent())
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

outcome_head = Outcome("Head")
outcome_tail = Outcome("Tail")

sample_space = SampleSpace([outcome_head, outcome_tail])


def prob_logic(event: BaseEvent) -> float:
  if event == Event(outcome_head):
    return 0.6
  if event == Event(outcome_tail):
    return 0.4


prob_function = ProbabilityFunction(prob_logic)
random_var = RandomVariable(prob_function, sample_space)

p_X = P__(random_var)
print(repr(p_X))
print(p_X(Event(outcome_head)).value)
print(p_X(Event(outcome_tail)).value)
print(p_X(Event(Outcome("Rain"))).value)
