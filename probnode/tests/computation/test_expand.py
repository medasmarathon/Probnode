from typing import List
import pytest
from probnode import p__X_, Event
from probnode.computation.expand import expand
from probnode.computation.util import _get_alternatives_from_list_of_possible_items
from probnode.probability.event import GenericSureEvent

from probnode.probability.event import *


def test_expand_atomic_event(atomic_event_1: AtomicEvent):
  assert expand(p__X_(atomic_event_1))[0] == p__X_(atomic_event_1)


def test_expand_complement_atomic_event(
    atomic_event_1: AtomicEvent, complement_atomic_event_1: ComplementaryAtomicEvent
    ):
  assert expand(p__X_(complement_atomic_event_1)
                )[0] == (p__X_(Event(GenericSureEvent())) - p__X_(atomic_event_1))


def test_expand_and_event(
    atomic_event_1: AtomicEvent,
    atomic_event_2: AtomicEvent,
    and_event: AndEvent,
    ):
  assert expand(p__X_(and_event)
                )[0] == (p__X_(atomic_event_1 // atomic_event_2) * p__X_(atomic_event_2))
  assert expand(p__X_(and_event)
                )[1] == (p__X_(atomic_event_2 // atomic_event_1) * p__X_(atomic_event_1))


def test_expand_or_event(
    atomic_event_1: AtomicEvent,
    atomic_event_2: AtomicEvent,
    or_event: OrEvent,
    and_event: AndEvent,
    ):
  assert expand(p__X_(or_event)
                )[0] == (p__X_(atomic_event_1) + p__X_(atomic_event_2) - p__X_(and_event))


def test_expand_conditional_event(
    atomic_event_1: AtomicEvent, atomic_event_2: AtomicEvent, or_event: OrEvent,
    and_event: AndEvent, conditional_event: ConditionalEvent
    ):
  assert expand(p__X_(conditional_event))[0] == (p__X_(and_event) / p__X_(atomic_event_2))


def test_expand_complex_probability_measure_chain(
    atomic_event_1: AtomicEvent, atomic_event_2: AtomicEvent, or_event: OrEvent,
    and_event: AndEvent, conditional_event: ConditionalEvent
    ):
  assert expand(p__X_(and_event) + p__X_(atomic_event_1))[0] == (
      p__X_(atomic_event_1 // atomic_event_2) * p__X_(atomic_event_2) + p__X_(atomic_event_1)
      )
  assert expand(p__X_(and_event) - p__X_(atomic_event_1))[1] == (
      p__X_(atomic_event_2 // atomic_event_1) * p__X_(atomic_event_1) - p__X_(atomic_event_1)
      )
  assert expand(p__X_(and_event) / p__X_(atomic_event_1))[1] == (
      p__X_(atomic_event_2 // atomic_event_1) * p__X_(atomic_event_1) / p__X_(atomic_event_1)
      )
  assert expand(p__X_(and_event) + p__X_(atomic_event_1.complement()))[1] == (
      p__X_(atomic_event_2 // atomic_event_1) * p__X_(atomic_event_1) +
      p__X_(Event(GenericSureEvent())) - p__X_(atomic_event_1)
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
