from typing import Callable
from probnode.computation.expand import expand

from probnode.probability.probability import SimpleProbabilityExpression


def test_expand_simple_prob_exp(
    simple_prob_expression: Callable[[str], SimpleProbabilityExpression]
    ):
  p1 = simple_prob_expression("Event 1")
  p2 = simple_prob_expression("Event 1")
  assert expand(p1) == p2