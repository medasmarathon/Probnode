from typing import List
import pytest
from probnode import N, P
from probnode.computation.expand import expand
from probnode.computation.util import _get_alternatives_from_list_of_possible_items
from probnode.probability.event import SureEvent

from probnode.probability.probability import *


def test_expand_simple_prob_exp(simple_prob_expression1: SimpleProbabilityExpression):
  assert expand(N(simple_prob_expression1))[0] == N(simple_prob_expression1)


def test_expand_invert_prob_exp(
    simple_prob_expression1: SimpleProbabilityExpression,
    simple_invert_prob_expression1: SimpleInvertProbabilityExpression
    ):
  assert expand(N(simple_invert_prob_expression1)
                )[0] == (N(P(SureEvent())) - N(simple_prob_expression1))


def test_expand_and_prob_exp(
    simple_prob_expression1: SimpleProbabilityExpression,
    simple_prob_expression2: SimpleProbabilityExpression,
    and_prob_expression: AndProbabilityExpression,
    ):
  assert expand(
      N(and_prob_expression)
      )[0] == (N(simple_prob_expression1 // simple_prob_expression2) * N(simple_prob_expression2))
  assert expand(
      N(and_prob_expression)
      )[1] == (N(simple_prob_expression2 // simple_prob_expression1) * N(simple_prob_expression1))


def test_expand_or_prob_exp(
    simple_prob_expression1: SimpleProbabilityExpression,
    simple_prob_expression2: SimpleProbabilityExpression,
    or_prob_expression: OrProbabilityExpression,
    and_prob_expression: AndProbabilityExpression,
    ):
  assert expand(
      N(or_prob_expression)
      )[0] == (N(simple_prob_expression1) + N(simple_prob_expression2) - N(and_prob_expression))


def test_expand_conditional_prob_exp(
    simple_prob_expression1: SimpleProbabilityExpression,
    simple_prob_expression2: SimpleProbabilityExpression,
    or_prob_expression: OrProbabilityExpression, and_prob_expression: AndProbabilityExpression,
    conditional_prob_expression: ConditionalProbabilityExpression
    ):
  assert expand(N(conditional_prob_expression)
                )[0] == (N(and_prob_expression) / N(simple_prob_expression2))


def test_expand_complex_prob_exp_chain(
    simple_prob_expression1: SimpleProbabilityExpression,
    simple_prob_expression2: SimpleProbabilityExpression,
    or_prob_expression: OrProbabilityExpression, and_prob_expression: AndProbabilityExpression,
    conditional_prob_expression: ConditionalProbabilityExpression
    ):
  assert expand(N(and_prob_expression) + N(simple_prob_expression1))[0] == (
      N(simple_prob_expression1 // simple_prob_expression2) * N(simple_prob_expression2) +
      N(simple_prob_expression1)
      )
  assert expand(N(and_prob_expression) - N(simple_prob_expression1))[1] == (
      N(simple_prob_expression2 // simple_prob_expression1) * N(simple_prob_expression1) -
      N(simple_prob_expression1)
      )
  assert expand(N(and_prob_expression) / N(simple_prob_expression1))[1] == (
      N(simple_prob_expression2 // simple_prob_expression1) * N(simple_prob_expression1) /
      N(simple_prob_expression1)
      )
  assert expand(N(and_prob_expression) + N(simple_prob_expression1.invert()))[1] == (
      N(simple_prob_expression2 // simple_prob_expression1) * N(simple_prob_expression1) + 1 -
      N(simple_prob_expression1)
      )


@pytest.mark.parametrize(
    ("input", "expect"),
    [([[], [1, 2, 3]], [[1], [2], [3]]), ([[1, 2, 3]], [[1], [2], [3]]),
     ([[1, 2, 3], [], []], [[1], [2], [3]]), ([[1, 2], [3]], [[1, 3], [2, 3]]),
     ([[1, 2], [3], [4, 5, 6]], [[1, 3, 4], [1, 3, 5], [1, 3, 6], [2, 3, 4], [2, 3, 5], [2, 3, 6]])]
    )
def test_get_alternatives_from_list_of_possible_items(
    input: List[List[int]], expect: List[List[int]]
    ):
  assert _get_alternatives_from_list_of_possible_items(input) == expect
