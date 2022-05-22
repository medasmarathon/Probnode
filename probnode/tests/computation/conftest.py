from typing import Callable
import pytest

from probnode import Outcome, Event, p__X_
from probnode.probability import *


@pytest.fixture(autouse=True)
def simple_prob_expression1():
  return Event(Outcome("Hot"))


@pytest.fixture(autouse=True)
def simple_prob_expression2():
  return Event(Outcome("Snow"))


@pytest.fixture(autouse=True)
def simple_invert_prob_expression1(simple_prob_expression1: AtomicEvent):
  return simple_prob_expression1.complement()


@pytest.fixture(autouse=True)
def simple_invert_prob_expression2(simple_prob_expression2: AtomicEvent):
  return simple_prob_expression2.complement()


@pytest.fixture(autouse=True)
def or_prob_expression(simple_prob_expression1, simple_prob_expression2):
  return Event(simple_prob_expression1 | simple_prob_expression2)


@pytest.fixture(autouse=True)
def and_prob_expression(simple_prob_expression1, simple_prob_expression2):
  return Event(simple_prob_expression1 & simple_prob_expression2)


@pytest.fixture(autouse=True)
def conditional_prob_expression(simple_prob_expression1, simple_prob_expression2):
  return Event(simple_prob_expression1 // simple_prob_expression2)