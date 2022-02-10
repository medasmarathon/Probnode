import pytest
from probnode import N, P
from probnode.computation.expand import expand
from probnode.probability.event import SureEvent

from probnode.probability.probability import *


def test_expand_simple_prob_exp(simple_prob_expression1: SimpleProbabilityExpression):
  assert expand(N(simple_prob_expression1)) == N(simple_prob_expression1)


def test_expand_invert_prob_exp(
    simple_prob_expression1: SimpleProbabilityExpression,
    simple_invert_prob_expression1: SimpleInvertProbabilityExpression
    ):
  assert expand(N(simple_invert_prob_expression1)
                ) == (N(P(SureEvent())) - N(simple_prob_expression1))


def test_expand_and_prob_exp(
    simple_prob_expression1: SimpleProbabilityExpression,
    simple_prob_expression2: SimpleProbabilityExpression,
    and_prob_expression: AndProbabilityExpression,
    ):
  assert expand(N(and_prob_expression)) == (N(simple_prob_expression1) * N(simple_prob_expression2))


def test_expand_or_prob_exp(
    simple_prob_expression1: SimpleProbabilityExpression,
    simple_prob_expression2: SimpleProbabilityExpression,
    or_prob_expression: OrProbabilityExpression,
    and_prob_expression: AndProbabilityExpression,
    ):
  assert expand(
      N(or_prob_expression)
      ) == (N(simple_prob_expression1) + N(simple_prob_expression2) - N(and_prob_expression))


def test_expand_conditional_prob_exp(
    simple_prob_expression1: SimpleProbabilityExpression,
    simple_prob_expression2: SimpleProbabilityExpression,
    or_prob_expression: OrProbabilityExpression, and_prob_expression: AndProbabilityExpression,
    conditional_prob_expression: ConditionalProbabilityExpression
    ):
  assert expand(N(conditional_prob_expression)
                ) == (N(and_prob_expression) / N(simple_prob_expression2))
