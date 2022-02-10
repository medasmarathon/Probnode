from typing import Callable
import pytest
from probnode import P

from probnode import Event
from probnode.probability.probability import SimpleProbabilityExpression


@pytest.fixture(autouse=True)
def simple_prob_expression1():
  return P(Event("Hot"))


@pytest.fixture(autouse=True)
def simple_prob_expression2():
  return P(Event("Snow"))


@pytest.fixture(autouse=True)
def simple_invert_prob_expression1(simple_prob_expression1: SimpleProbabilityExpression):
  return simple_prob_expression1.invert()


@pytest.fixture(autouse=True)
def simple_invert_prob_expression2(simple_prob_expression2: SimpleProbabilityExpression):
  return simple_prob_expression2.invert()


@pytest.fixture(autouse=True)
def or_prob_expression(simple_prob_expression1, simple_prob_expression2):
  return P(simple_prob_expression1 | simple_prob_expression2)


@pytest.fixture(autouse=True)
def and_prob_expression(simple_prob_expression1, simple_prob_expression2):
  return P(simple_prob_expression1 & simple_prob_expression2)


@pytest.fixture(autouse=True)
def conditional_prob_expression(simple_prob_expression1, simple_prob_expression2):
  return P(simple_prob_expression1 // simple_prob_expression2)