from collections import Counter
from typing import List, Tuple
import pytest
from probnode import *
from probnode.computation.contract import *


def test_contract():
  sure_event = GenericSureEvent()
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  event_y_and_x = event_y & event_x
  event_x_or_y = event_x | event_y
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  p_y_and_x = ProbabilityMeasureOfEvent(event_y_and_x)
  p_y_when_x = ProbabilityMeasureOfEvent(event_y // event_x)
  p_x_when_y = ProbabilityMeasureOfEvent(event_x // event_y)

  chain_1 = ProbabilityMeasureOfEvent(event_x) + ProbabilityMeasureOfEvent(
      event_y
      ) - ProbabilityMeasureOfEvent(event_x_and_y)
  chain_2 = chain_1 + ProbabilityMeasureOfEvent(sure_event)
  chain_3 = ProbabilityMeasureOfEvent(event_x) - ProbabilityMeasureOfEvent(
      event_x_and_y
      ) + ProbabilityMeasureOfEvent(event_y)
  chain_4 = ProbabilityMeasureOfEvent(event_x) - ProbabilityMeasureOfEvent(
      event_x_and_y
      ) + ProbabilityMeasureOfEvent(event_y) * ProbabilityMeasureOfEvent(
          event_z
          ) + ProbabilityMeasureOfEvent(event_y)
  chain_5 = ProbabilityMeasureOfEvent(event_x) - ProbabilityMeasureOfEvent(
      event_x_and_y
      ) + ProbabilityMeasureOfEvent(event_y) * ProbabilityMeasureOfEvent(
          event_z
          ) + ProbabilityMeasureOfEvent(event_y) - ProbabilityMeasureOfEvent(event_y)
  chain_6 = ProbabilityMeasureOfEvent(event_x) - ProbabilityMeasureOfEvent(
      event_x_and_y
      ) + ProbabilityMeasureOfEvent(event_y) * ProbabilityMeasureOfEvent(
          event_z
          ) + ProbabilityMeasureOfEvent(event_y) - ProbabilityMeasureOfEvent(
              event_y
              ) + ProbabilityMeasureOfEvent(event_x
                                            ) * ProbabilityMeasureOfEvent(event_y) * p_y_when_x

  assert contract(SumP()) == SumP()
  assert contract(chain_1) == ProbabilityMeasureOfEvent(event_x_or_y)
  assert contract(chain_2) == (
      ProbabilityMeasureOfEvent(sure_event) + ProbabilityMeasureOfEvent(event_x_or_y)
      )
  assert contract(chain_3) == ProbabilityMeasureOfEvent(event_x_or_y)
  assert contract(chain_4) == ProbabilityMeasureOfEvent(event_y) * ProbabilityMeasureOfEvent(
      event_z
      ) + ProbabilityMeasureOfEvent(event_x_or_y)
  assert contract(chain_5) == ProbabilityMeasureOfEvent(event_y) * ProbabilityMeasureOfEvent(
      event_z
      ) + ProbabilityMeasureOfEvent(event_x) - ProbabilityMeasureOfEvent(event_x_and_y)
  assert contract(chain_6).is_permutation_of(
      ProbabilityMeasureOfEvent(event_y) * ProbabilityMeasureOfEvent(event_z) +
      ProbabilityMeasureOfEvent(event_x) - ProbabilityMeasureOfEvent(event_x_and_y) +
      ProbabilityMeasureOfEvent(event_y) * p_y_and_x
      )


def test_replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
):
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  event_x_or_y = event_x | event_y
  assert replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
      [], []
      ) == ([], [])
  assert replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
      [event_x], []
      ) == ([event_x], [])
  assert replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
      [], [event_x_and_y]
      ) == ([], [event_x_and_y])
  assert replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
      [event_x], [event_x_and_y]
      ) == ([event_x], [event_x_and_y])
  assert replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
      [event_x, event_y], [event_x_and_y]
      ) == ([event_x_or_y], [])
  assert replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
      [event_x, event_y, event_z], [event_x_and_y]
      ) == ([event_z, event_x_or_y], [])
  assert replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
      [event_x, event_z, event_y], [event_x_and_y]
      ) == ([event_z, event_x_or_y], [])
  assert replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
      [event_x, event_y, event_y], [event_x_and_y]
      ) == ([event_y, event_x_or_y], [])
  assert replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
      [event_x, event_x, event_y], [event_x_and_y]
      ) == ([event_x, event_x_or_y], [])


def test_remove_or_event_pattern_Ps_from_classified_lists():
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  p_x_or_y = ProbabilityMeasureOfEvent(event_x | event_y)
  inverted_p_x_and_y = p_x_and_y.additive_invert()
  assert remove_or_event_pattern_Ps_from_classified_lists([], []) == ([], [])
  assert remove_or_event_pattern_Ps_from_classified_lists([p_x], []) == ([p_x], [])
  assert remove_or_event_pattern_Ps_from_classified_lists([], [inverted_p_x_and_y]) == ([], [
      inverted_p_x_and_y
      ])
  assert remove_or_event_pattern_Ps_from_classified_lists([p_x], [inverted_p_x_and_y]) == ([p_x], [
      inverted_p_x_and_y
      ])
  assert remove_or_event_pattern_Ps_from_classified_lists([p_x, p_y],
                                                          [inverted_p_x_and_y]) == ([p_x_or_y], [])
  assert remove_or_event_pattern_Ps_from_classified_lists([p_x, p_y, p_z],
                                                          [inverted_p_x_and_y]) == ([p_z,
                                                                                     p_x_or_y], [])
  assert remove_or_event_pattern_Ps_from_classified_lists([p_x, p_z, p_y],
                                                          [inverted_p_x_and_y]) == ([p_z,
                                                                                     p_x_or_y], [])
  assert remove_or_event_pattern_Ps_from_classified_lists([p_x, p_y, p_y],
                                                          [inverted_p_x_and_y]) == ([p_y,
                                                                                     p_x_or_y], [])
  assert remove_or_event_pattern_Ps_from_classified_lists([p_x, p_x, p_y],
                                                          [inverted_p_x_and_y]) == ([p_x,
                                                                                     p_x_or_y], [])


def test_remove_negating_Ps_from_classified_lists():
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  inverted_p_x_and_y = p_x_and_y.additive_invert()
  inverted_p_x = p_x.additive_invert()
  inverted_p_y = p_y.additive_invert()
  assert remove_negating_Ps_from_classified_lists([], []) == ([], [])
  assert remove_negating_Ps_from_classified_lists([p_x_and_y], [inverted_p_x_and_y]) == ([], [])
  assert remove_negating_Ps_from_classified_lists([],
                                                  [inverted_p_x_and_y]) == ([],
                                                                            [inverted_p_x_and_y])
  assert remove_negating_Ps_from_classified_lists([p_x, p_x_and_y],
                                                  [inverted_p_x_and_y]) == ([p_x], [])
  assert remove_negating_Ps_from_classified_lists([p_x, p_x], []) == ([p_x, p_x], [])
  assert remove_negating_Ps_from_classified_lists([p_x, p_x, p_y], [inverted_p_x]) == ([p_x,
                                                                                        p_y], [])
  assert remove_negating_Ps_from_classified_lists([p_x, p_x, p_y],
                                                  [inverted_p_x, inverted_p_y]) == ([p_x], [])
  assert remove_negating_Ps_from_classified_lists([p_y],
                                                  [inverted_p_x, inverted_p_y]) == ([],
                                                                                    [inverted_p_x])


def test_contract_complement_Ps():
  sure_event = GenericSureEvent()
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  p_1 = ProbabilityMeasureOfEvent(sure_event)
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  p_not_x = ProbabilityMeasureOfEvent(event_x.complement())
  p_not_y = ProbabilityMeasureOfEvent(event_y.complement())
  p_not_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y.complement())

  sum = SumP()
  sum.args = [2]
  assert contract_complement_Ps(sum).args == [2]

  assert contract_complement_Ps(p_x + p_y).args == [p_x, p_y]
  assert contract_complement_Ps(p_1 - p_y).args == [p_not_y]
  assert contract_complement_Ps(2 + p_x + p_y + p_1).args == [3, p_x, p_y]
  assert contract_complement_Ps(2 + p_x - p_not_y).args == [1, p_x, p_y]
  assert contract_complement_Ps(1 + p_1 - p_not_y - p_not_x_and_y).args == [p_y, p_x_and_y]


def test_contract_negating_Ps():
  sure_event = GenericSureEvent()
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  p_1 = ProbabilityMeasureOfEvent(sure_event)
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  p_not_x = ProbabilityMeasureOfEvent(event_x.complement())
  p_not_y = ProbabilityMeasureOfEvent(event_y.complement())
  p_not_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y.complement())

  sum = SumP()
  sum.args = [2]
  assert contract_negating_Ps(sum).args == [2]

  assert contract_negating_Ps(p_x + p_y).args == [p_x, p_y]
  assert contract_negating_Ps(p_y - p_y).args == []
  assert contract_negating_Ps(2 + p_x + p_y + p_1).args == [3, p_x, p_y]
  assert contract_negating_Ps(2 + p_x - p_1).args == [1, p_x]
  assert contract_negating_Ps(1 + p_x_and_y - p_y - p_x_and_y).args == [1, -p_y]


def test_remove_complement_Ps_from_classified_lists():
  sure_event = GenericSureEvent()
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  p_1 = ProbabilityMeasureOfEvent(sure_event)
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  p_not_x = ProbabilityMeasureOfEvent(event_x.complement())
  p_not_y = ProbabilityMeasureOfEvent(event_y.complement())
  p_not_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y.complement())
  assert remove_complement_Ps_from_classified_lists(2, [], []) == (2, [], [])
  assert remove_complement_Ps_from_classified_lists(2, [p_x, p_y, p_1],
                                                    []) == (2, [p_x, p_y, p_1], [])
  assert remove_complement_Ps_from_classified_lists(2, [p_x], [p_not_y]) == (2, [p_x], [p_not_y])
  assert remove_complement_Ps_from_classified_lists(2, [p_y], [p_not_y]) == (2, [p_y], [p_not_y])
  assert remove_complement_Ps_from_classified_lists(2, [p_1], [p_not_y.additive_invert()
                                                               ]) == (1, [p_1, p_y], [])
  assert remove_complement_Ps_from_classified_lists(2, [p_1, p_1], [p_not_y.additive_invert()
                                                                    ]) == (1, [p_1, p_1, p_y], [])
  assert remove_complement_Ps_from_classified_lists(
      2, [p_1, p_1, p_1], [p_x.additive_invert(), p_y.additive_invert()]
      ) == (0, [p_1, p_1, p_1, p_not_x, p_not_y], [])
  assert remove_complement_Ps_from_classified_lists(
      2, [p_1], [p_x.additive_invert(), p_x_and_y.additive_invert()]
      ) == (0, [p_1, p_not_x, p_not_x_and_y], [])
  assert remove_complement_Ps_from_classified_lists(
      2, [p_1], [p_x.additive_invert(), p_x_and_y.additive_invert(), p_z]
      ) == (0, [p_1, p_not_x, p_not_x_and_y], [p_z])


def test_contract_arbitrary_sum_P_group():
  sure_event = GenericSureEvent()
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  event_x_or_y = event_x | event_y
  p_1 = ProbabilityMeasureOfEvent(sure_event)
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  p_not_x = ProbabilityMeasureOfEvent(event_x.complement())
  p_not_y = ProbabilityMeasureOfEvent(event_y.complement())
  p_x_or_y = ProbabilityMeasureOfEvent(event_x_or_y)

  assert contract_arbitrary_sum_P_group([]) == []
  assert contract_arbitrary_sum_P_group([p_x]) == [p_x]
  assert contract_arbitrary_sum_P_group([p_x, p_x, p_y]) == [p_x, p_x, p_y]
  assert contract_arbitrary_sum_P_group([p_x, p_x.additive_invert(), p_y]) == [p_y]
  assert contract_arbitrary_sum_P_group([p_1, p_x, p_x.additive_invert(), p_y]) == [1.0, p_y]
  assert contract_arbitrary_sum_P_group([
      p_1, p_x, p_x.additive_invert(), p_x.additive_invert(), p_y
      ]) == [p_y, p_not_x]
  assert contract_arbitrary_sum_P_group([
      p_1, p_x,
      p_x.additive_invert(),
      p_x.additive_invert(), p_x, p_y,
      p_x_and_y.additive_invert()
      ]) == [p_y, ProbabilityMeasureOfEvent(event_x_and_y.complement())]
  assert contract_arbitrary_sum_P_group([p_1, p_x, p_y,
                                         p_x_and_y.additive_invert()]) == [1.0, p_x_or_y]
  assert contract_arbitrary_sum_P_group([p_1, p_x, p_y, p_not_y,
                                         p_x_and_y.additive_invert()]) == [1.0, p_not_y, p_x_or_y]
  assert contract_arbitrary_sum_P_group([
      p_1, p_x, p_y, p_not_y.additive_invert(),
      p_x_and_y.additive_invert()
      ]) == [p_x_or_y, p_y]


def test_replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent():
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  event_y_when_x = event_y // event_x
  event_x_when_y = event_x // event_y
  assert replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent([], []) == ([], [])
  assert replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent([event_x],
                                                                           []) == ([event_x], [])
  assert replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent([],
                                                                           [event_x_and_y
                                                                            ]) == ([],
                                                                                   [event_x_and_y])
  assert replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent([event_x],
                                                                           [event_x_and_y
                                                                            ]) == ([],
                                                                                   [event_y_when_x])
  assert replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent([event_x, event_y],
                                                                           [event_x_and_y]) == ([
                                                                               event_y
                                                                               ], [event_y_when_x])
  assert replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent([
      event_x, event_y, event_z
      ], [event_x_and_y]) == ([event_y, event_z], [event_y_when_x])
  assert replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent([
      event_y, event_z, event_x
      ], [event_x_and_y]) == ([event_z, event_x], [event_x_when_y])
  assert replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent([
      event_x, event_y, event_y
      ], [event_x_and_y]) == ([event_y, event_y], [event_y_when_x])
  assert replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent([
      event_x, event_x, event_y
      ], [event_x_and_y]) == ([event_x, event_y], [event_y_when_x])


def test_simplify_Ps_of_ConditionalEvent_from_classified_lists():
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x & event_y)
  p_y_when_x = ProbabilityMeasureOfEvent(event_y // event_x)
  p_x_when_y = ProbabilityMeasureOfEvent(event_x // event_y)
  assert simplify_Ps_of_ConditionalEvent_from_classified_lists([], []) == ([], [])
  assert simplify_Ps_of_ConditionalEvent_from_classified_lists([p_x], []) == ([p_x], [])
  assert simplify_Ps_of_ConditionalEvent_from_classified_lists([],
                                                               [p_x_when_y]) == ([], [p_x_when_y])
  assert simplify_Ps_of_ConditionalEvent_from_classified_lists([p_x_and_y],
                                                               [p_x.reciprocate()]) == ([
                                                                   p_y_when_x
                                                                   ], [])
  assert simplify_Ps_of_ConditionalEvent_from_classified_lists([p_x_and_y], [
      p_x.reciprocate(), p_y.reciprocate()
      ]) == ([p_y_when_x], [p_y.reciprocate()])
  assert simplify_Ps_of_ConditionalEvent_from_classified_lists([p_x_and_y], [
      p_x.reciprocate(), p_y.reciprocate(), p_z.reciprocate()
      ]) == ([p_y_when_x], [p_y.reciprocate(), p_z.reciprocate()])
  assert simplify_Ps_of_ConditionalEvent_from_classified_lists([p_x_and_y], [
      p_y.reciprocate(), p_x.reciprocate(), p_z.reciprocate()
      ]) == ([p_x_when_y], [p_x.reciprocate(), p_z.reciprocate()])
  assert simplify_Ps_of_ConditionalEvent_from_classified_lists([p_x_and_y], [
      p_x.reciprocate(), p_y.reciprocate(), p_y.reciprocate()
      ]) == ([p_y_when_x], [p_y.reciprocate(), p_y.reciprocate()])
  assert simplify_Ps_of_ConditionalEvent_from_classified_lists([p_x_and_y], [
      p_x.reciprocate(), p_x.reciprocate(), p_y.reciprocate()
      ]) == ([p_y_when_x], [p_x.reciprocate(), p_y.reciprocate()])


def test_contract_arbitrary_product_P_group():
  sure_event = GenericSureEvent()
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  event_y_and_x = event_y & event_x
  event_x_or_y = event_x | event_y
  p_1 = ProbabilityMeasureOfEvent(sure_event)
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  p_y_and_x = ProbabilityMeasureOfEvent(event_y_and_x)
  p_y_when_x = ProbabilityMeasureOfEvent(event_y // event_x)
  p_x_when_y = ProbabilityMeasureOfEvent(event_x // event_y)

  assert contract_arbitrary_product_P_group([]) == []
  assert contract_arbitrary_product_P_group([p_x]) == [p_x]
  assert contract_arbitrary_product_P_group([p_x, p_x, p_y]) == [p_x, p_x, p_y]
  assert contract_arbitrary_product_P_group([p_x, p_x.reciprocate(), p_y]) == [p_y]
  assert contract_arbitrary_product_P_group([p_1, p_x, p_x.reciprocate(), p_y]) == [p_y]
  assert contract_arbitrary_product_P_group([p_1, p_x,
                                             p_x.reciprocate(),
                                             p_x.reciprocate(), p_y]) == [p_y,
                                                                          p_x.reciprocate()]
  assert contract_arbitrary_product_P_group([
      p_1, p_x, p_x.reciprocate(),
      p_x.reciprocate(), p_x, p_y, p_x_and_y
      ]) == [p_y, p_x_and_y]
  assert contract_arbitrary_product_P_group([p_1, p_x, p_y.reciprocate(),
                                             p_x_and_y]) == [p_x, p_x_when_y]
  assert contract_arbitrary_product_P_group([p_x, p_x, p_y_when_x]) == [p_x, p_y_and_x]
  assert contract_arbitrary_product_P_group([p_y, p_x, p_y_when_x,
                                             p_x_when_y]) == [p_y_and_x, p_x_and_y]


def test_contract_reciprocated_Ps():
  sure_event = GenericSureEvent()
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  p_1 = ProbabilityMeasureOfEvent(sure_event)
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  p_not_x = ProbabilityMeasureOfEvent(event_x.complement())
  p_not_y = ProbabilityMeasureOfEvent(event_y.complement())
  p_not_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y.complement())

  sum = ProductP()
  sum.args = [2]
  assert contract_reciprocated_Ps(sum).args == [2]

  assert contract_reciprocated_Ps(p_x * p_y).args == [p_x, p_y]
  assert contract_reciprocated_Ps(p_y / p_y).args == []
  assert contract_reciprocated_Ps(2 * p_x / p_y * p_1).args == [2, p_x, p_y.reciprocate()]
  assert contract_reciprocated_Ps(p_x_and_y * p_x / p_x_and_y / 0.5).args == [2, p_x]


def test_contract_Ps_of_ConditionalEvent():
  sure_event = GenericSureEvent()
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  event_x_when_y = event_x // event_y
  p_1 = ProbabilityMeasureOfEvent(sure_event)
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  p_x_when_y = ProbabilityMeasureOfEvent(event_x_when_y)
  p_not_x = ProbabilityMeasureOfEvent(event_x.complement())
  p_not_y = ProbabilityMeasureOfEvent(event_y.complement())
  p_not_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y.complement())

  sum = ProductP()
  sum.args = [2]
  assert contract_Ps_of_ConditionalEvent(sum).args == [2.0]

  assert contract_Ps_of_ConditionalEvent(p_x * p_y).args == [p_x, p_y]
  assert contract_Ps_of_ConditionalEvent(p_x_and_y / p_y).args == [p_x_when_y]
  assert contract_Ps_of_ConditionalEvent(2 * p_x / p_y * p_1).args == [2, p_x, p_y.reciprocate()]
  assert contract_Ps_of_ConditionalEvent(p_x_and_y / p_y / 0.5).args == [2, p_x_when_y]


def test_contract_expanded_Ps_of_AndEvent():
  sure_event = GenericSureEvent()
  event_x = Event(Outcome("x"))
  event_y = Event(Outcome("y"))
  event_z = Event(Outcome("z"))
  event_x_and_y = event_x & event_y
  event_x_when_y = event_x // event_y
  p_1 = ProbabilityMeasureOfEvent(sure_event)
  p_x = ProbabilityMeasureOfEvent(event_x)
  p_y = ProbabilityMeasureOfEvent(event_y)
  p_z = ProbabilityMeasureOfEvent(event_z)
  p_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y)
  p_x_when_y = ProbabilityMeasureOfEvent(event_x_when_y)
  p_not_x = ProbabilityMeasureOfEvent(event_x.complement())
  p_not_y = ProbabilityMeasureOfEvent(event_y.complement())
  p_not_x_and_y = ProbabilityMeasureOfEvent(event_x_and_y.complement())

  sum = ProductP()
  sum.args = [2]
  assert contract_expanded_Ps_of_AndEvent(sum).args == [2.0]

  assert contract_expanded_Ps_of_AndEvent(p_x * p_y).args == [p_x, p_y]
  assert contract_expanded_Ps_of_AndEvent(p_x_and_y / p_y).args == [p_x_and_y, p_y.reciprocate()]
  assert contract_expanded_Ps_of_AndEvent(p_x_when_y * p_y).args == [p_x_and_y]
  assert contract_expanded_Ps_of_AndEvent(2 * p_x_when_y / p_y * p_y
                                          ).args == [2.0, p_x_and_y,
                                                     p_y.reciprocate()]
