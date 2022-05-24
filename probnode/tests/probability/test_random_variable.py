from probnode import Outcome, SampleSpace
from probnode.probability.event import AtomicEvent, BaseEvent, Event
from probnode.datatype import ProbabilityFunction
from probnode.probability import RandomVariable
from probnode.probability.probability_measure import ProbMeasure_with_RandomVar


def test_simple_random_var_with_prob_function():
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

  p_X = ProbMeasure_with_RandomVar(random_var)
  assert p_X(Event(outcome_head)).value == 0.6
  assert p_X(Event(outcome_tail)).value == 0.4
  assert p_X(Event(Outcome("Rain"))).value == float(0)