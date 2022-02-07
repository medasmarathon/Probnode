from typing import Callable
import pytest
from probnode import P

from probnode import Event
from probnode.probability.probability import SimpleProbabilityExpression


@pytest.fixture(autouse=True)
def simple_prob_expression(evt_name: str):
  return P(Event(evt_name))


@pytest.fixture(autouse=True)
def simple_invert_prob_expression(evt_name: str):
  return simple_prob_expression(evt_name).invert()


@pytest.fixture(autouse=True)
def or_prob_expression():
  p1 = simple_prob_expression("Hot")
  p2 = simple_prob_expression("Rain")
  return P(p1 | p2)


@pytest.fixture(autouse=True)
def and_prob_expression():
  p1 = simple_prob_expression("Cold")
  p2 = simple_prob_expression("Snow")
  return P(p1 & p2)


@pytest.fixture(autouse=True)
def conditional_prob_expression():
  p1 = simple_prob_expression("Hot")
  p2 = simple_prob_expression("Winter")
  return P(p1 // p2)