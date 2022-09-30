from typing import Optional
from probnode.computation.evaluate import eval_p
from probnode import Outcome, Event, P__, ProbabilityDistribution, SampleSpace, RandomVariable, BaseEvent, GenericSureEvent, DiscreteOutcome, RangeOutcome, Range

outcome1 = Outcome("Outcome 1")
outcome1_event = Event(outcome1)
outcome2 = Outcome("Outcome 2")
outcome2_event = Event(outcome2)

outcome_1_or_2_event = outcome1_event | outcome2_event     # Or events
outcome_1_and_2_event = outcome1_event & outcome2_event     # And events
outcome_1_when_2_event = outcome1_event // outcome2_event     # Conditional event

# Display mathematical representation of the object(s)
print(repr(outcome1_event))

# Probability of events
from probnode import ProbabilityMeasureOfEvent

p_1 = ProbabilityMeasureOfEvent(outcome1_event)     # Each below is a probability measure
p_2 = ProbabilityMeasureOfEvent(outcome2_event)
p_1_or_2 = ProbabilityMeasureOfEvent(outcome_1_or_2_event)
p_1_and_2 = ProbabilityMeasureOfEvent(outcome_1_and_2_event)
p_1_when_2 = ProbabilityMeasureOfEvent(outcome_1_when_2_event)

# A sum of nodes
sum_p = 2.0 + p_1 + p_2 - 1 - p_1_and_2 + ProbabilityMeasureOfEvent(GenericSureEvent())
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


@ProbabilityDistribution
def prob_logic(event: BaseEvent) -> Optional[float]:
  match event:
    case event if (event == Event(outcome_head)):
      return 0.6
    case event if (event == Event(outcome_tail)):
      return 0.4
  return None


random_var = RandomVariable(prob_logic, sample_space)

p_X = P__(random_var)
print(repr(p_X))
print(eval_p(p_X(Event(outcome_head))))
print(eval_p(p_X(Event(outcome_tail))))
print(eval_p(p_X(Event(Outcome("Rain")))))

outcome_head_1st_try = Outcome("1st Head")
outcome_tail_1st_try = Outcome("1st Tail")
outcome_head_2nd_try = Outcome("2nd Head")
outcome_tail_2nd_try = Outcome("2nd Tail")

sample_space_complex = SampleSpace([
    outcome_head_1st_try, outcome_head_2nd_try, outcome_tail_1st_try, outcome_tail_2nd_try
    ])

discrete_outcome_1 = DiscreteOutcome("discrete", 1)

discrete_outcome_2 = DiscreteOutcome("discrete", "two")
print(discrete_outcome_1 == discrete_outcome_2)

range_outcome = RangeOutcome("mark", Range(2, "upper"))
print(range_outcome)