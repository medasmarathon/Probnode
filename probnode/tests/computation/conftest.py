from typing import Callable
import pytest

from probnode import Outcome, Event, p__X_
from probnode.probability import *


@pytest.fixture(autouse=True)
def atomic_event_1():
  return Event(Outcome("Hot"))


@pytest.fixture(autouse=True)
def atomic_event_2():
  return Event(Outcome("Snow"))


@pytest.fixture(autouse=True)
def complement_atomic_event_1(atomic_event_1: AtomicEvent):
  return atomic_event_1.complement()


@pytest.fixture(autouse=True)
def complement_atomic_event_2(atomic_event_2: AtomicEvent):
  return atomic_event_2.complement()


@pytest.fixture(autouse=True)
def or_event(atomic_event_1, atomic_event_2):
  return Event(atomic_event_1 | atomic_event_2)


@pytest.fixture(autouse=True)
def and_event(atomic_event_1, atomic_event_2):
  return Event(atomic_event_1 & atomic_event_2)


@pytest.fixture(autouse=True)
def conditional_event(atomic_event_1, atomic_event_2):
  return Event(atomic_event_1 // atomic_event_2)