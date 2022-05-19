from typing import Callable
import pytest

from probnode import Outcome, ES, P_X
from probnode.probability import *


@pytest.fixture(autouse=True)
def simple_prob_expression1():
  return ES(Outcome("Hot"))


@pytest.fixture(autouse=True)
def simple_prob_expression2():
  return ES(Outcome("Snow"))


@pytest.fixture(autouse=True)
def simple_invert_prob_expression1(simple_prob_expression1: SimpleEventSet):
  return simple_prob_expression1.invert()


@pytest.fixture(autouse=True)
def simple_invert_prob_expression2(simple_prob_expression2: SimpleEventSet):
  return simple_prob_expression2.invert()


@pytest.fixture(autouse=True)
def or_prob_expression(simple_prob_expression1, simple_prob_expression2):
  return ES(simple_prob_expression1 | simple_prob_expression2)


@pytest.fixture(autouse=True)
def and_prob_expression(simple_prob_expression1, simple_prob_expression2):
  return ES(simple_prob_expression1 & simple_prob_expression2)


@pytest.fixture(autouse=True)
def conditional_prob_expression(simple_prob_expression1, simple_prob_expression2):
  return ES(simple_prob_expression1 // simple_prob_expression2)