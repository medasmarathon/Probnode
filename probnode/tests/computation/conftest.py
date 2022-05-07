from typing import Callable
import pytest

from probnode import Outcome, P, N
from probnode.probability import *


@pytest.fixture(autouse=True)
def simple_prob_expression1():
  return P(Outcome("Hot"))


@pytest.fixture(autouse=True)
def simple_prob_expression2():
  return P(Outcome("Snow"))


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