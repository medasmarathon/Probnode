from probnode import Outcome, SampleSpace
from probnode.probability.event import AtomicEvent, BaseEvent, Event
from probnode.probability import ProbabilityDistribution
from probnode.probability import RandomVariable
from probnode.probability.probability_measure import P__
from probnode.computation import eval_p


def test_simple_random_var_with_prob_function():
  outcome_head = Outcome("Head")
  outcome_tail = Outcome("Tail")

  sample_space = SampleSpace([outcome_head, outcome_tail])

  def prob_logic(event: BaseEvent) -> float:
    if event == Event(outcome_head):
      return 0.6
    if event == Event(outcome_tail):
      return 0.4

  prob_function = ProbabilityDistribution(prob_logic)
  random_var = RandomVariable(prob_function, sample_space)

  p_X = P__(random_var)
  assert eval_p(p_X(Event(outcome_head))) == 0.6
  assert eval_p(p_X(Event(outcome_tail))) == 0.4
  assert eval_p(p_X(Event(Outcome("Rain")))) == None