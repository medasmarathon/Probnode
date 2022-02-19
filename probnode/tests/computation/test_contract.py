from typing import List, Tuple
import pytest
from probnode import *
from probnode.computation.contract import *


def test_remove_same_exp_in_simple_vs_and_prob_lists():
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  assert remove_same_exp_in_simple_vs_and_prob_lists([], []) == ([], [])
  assert remove_same_exp_in_simple_vs_and_prob_lists([prob_x], []) == ([prob_x], [])
  assert remove_same_exp_in_simple_vs_and_prob_lists([], [prob_x_and_y]) == ([], [prob_x_and_y])
  assert remove_same_exp_in_simple_vs_and_prob_lists([prob_x],
                                                     [prob_x_and_y]) == ([prob_x], [prob_x_and_y])
  assert remove_same_exp_in_simple_vs_and_prob_lists([prob_x, prob_y], [prob_x_and_y]) == ([], [])
  assert remove_same_exp_in_simple_vs_and_prob_lists([prob_x, prob_y, prob_z],
                                                     [prob_x_and_y]) == ([prob_z], [])
  assert remove_same_exp_in_simple_vs_and_prob_lists([prob_x, prob_z, prob_y],
                                                     [prob_x_and_y]) == ([prob_z], [])
  assert remove_same_exp_in_simple_vs_and_prob_lists([prob_x, prob_y, prob_y],
                                                     [prob_x_and_y]) == ([prob_y], [])
  assert remove_same_exp_in_simple_vs_and_prob_lists([prob_x, prob_x, prob_y],
                                                     [prob_x_and_y]) == ([prob_x], [])


def test_contract_or_prob_pattern_nodes():
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  node_x = Node(prob_x)
  node_y = Node(prob_y)
  node_z = Node(prob_z)
  node_x_and_y = Node(prob_x_and_y)
  inverted_node_x_and_y = additive_invert(node_x_and_y)
  assert contract_or_prob_pattern_nodes([], []) == ([], [])
  assert contract_or_prob_pattern_nodes([node_x], []) == ([node_x], [])
  assert contract_or_prob_pattern_nodes([],
                                        [inverted_node_x_and_y]) == ([], [inverted_node_x_and_y])
  assert contract_or_prob_pattern_nodes([node_x],
                                        [inverted_node_x_and_y]) == ([node_x],
                                                                     [inverted_node_x_and_y])
  assert contract_or_prob_pattern_nodes([node_x, node_y], [inverted_node_x_and_y]) == ([], [])
  assert contract_or_prob_pattern_nodes([node_x, node_y, node_z],
                                        [inverted_node_x_and_y]) == ([node_z], [])
  assert contract_or_prob_pattern_nodes([node_x, node_z, node_y],
                                        [inverted_node_x_and_y]) == ([node_z], [])
  assert contract_or_prob_pattern_nodes([node_x, node_y, node_y],
                                        [inverted_node_x_and_y]) == ([node_y], [])
  assert contract_or_prob_pattern_nodes([node_x, node_x, node_y],
                                        [inverted_node_x_and_y]) == ([node_x], [])


def test_contract_negating_nodes():
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  node_x = Node(prob_x)
  node_y = Node(prob_y)
  node_z = Node(prob_z)
  node_x_and_y = Node(prob_x_and_y)
  inverted_node_x_and_y = additive_invert(node_x_and_y)
  inverted_node_x = additive_invert(node_x)
  inverted_node_y = additive_invert(node_y)
  assert contract_negating_nodes([], []) == ([], [])
  assert contract_negating_nodes([node_x_and_y], [inverted_node_x_and_y]) == ([], [])
  assert contract_negating_nodes([], [inverted_node_x_and_y]) == ([], [inverted_node_x_and_y])
  assert contract_negating_nodes([node_x, node_x_and_y], [inverted_node_x_and_y]) == ([node_x], [])
  assert contract_negating_nodes([node_x, node_x], []) == ([node_x, node_x], [])
  assert contract_negating_nodes([node_x, node_x, node_y], [inverted_node_x]) == ([node_x,
                                                                                   node_y], [])
  assert contract_negating_nodes([node_x, node_x, node_y],
                                 [inverted_node_x, inverted_node_y]) == ([node_x], [])
  assert contract_negating_nodes([node_y],
                                 [inverted_node_x, inverted_node_y]) == ([], [inverted_node_x])


def test_contract_complement_nodes():
  sure_prob = P(SureEvent())
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  node_1 = Node(sure_prob)
  node_x = Node(prob_x)
  node_y = Node(prob_y)
  node_z = Node(prob_z)
  node_x_and_y = Node(prob_x_and_y)
  node_not_x = Node(prob_x.invert())
  node_not_y = Node(prob_y.invert())
  node_not_x_and_y = Node(prob_x_and_y.invert())
  assert contract_complement_nodes([], []) == ([], [])
  assert contract_complement_nodes([node_x, node_y, node_1], []) == ([node_x, node_y, node_1], [])
  assert contract_complement_nodes([node_x], [node_not_y]) == ([node_x], [node_not_y])
  assert contract_complement_nodes([node_y], [node_not_y]) == ([node_y], [node_not_y])
  assert contract_complement_nodes([node_1], [additive_invert(node_not_y)]) == ([node_y], [])
  assert contract_complement_nodes([node_1, node_1],
                                   [additive_invert(node_not_y)]) == ([node_1, node_y], [])
  assert contract_complement_nodes([node_1, node_1, node_1],
                                   [additive_invert(node_x),
                                    additive_invert(node_y)]) == ([node_1, node_not_x,
                                                                   node_not_y], [])
  assert contract_complement_nodes([node_1, node_1, node_1],
                                   [additive_invert(node_x),
                                    additive_invert(node_x_and_y)]) == ([
                                        node_1, node_not_x, node_not_x_and_y
                                        ], [])
  assert contract_complement_nodes([node_1, node_1, node_1],
                                   [additive_invert(node_x),
                                    additive_invert(node_x_and_y), node_z]) == ([
                                        node_1, node_not_x, node_not_x_and_y
                                        ], [node_z])


def test_contract_arbitrary_sum_node_group():
  sure_prob = P(SureEvent())
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  prob_x_or_y = P(prob_x | prob_y)
  node_1 = Node(sure_prob)
  node_x = Node(prob_x)
  node_y = Node(prob_y)
  node_z = Node(prob_z)
  node_x_and_y = Node(prob_x_and_y)
  node_not_x = Node(prob_x.invert())
  node_not_y = Node(prob_y.invert())
  node_x_or_y = Node(prob_x_or_y)

  assert contract_arbitrary_sum_node_group([]) == []
  assert contract_arbitrary_sum_node_group([node_x]) == [node_x]
  assert contract_arbitrary_sum_node_group([node_x, node_x, node_y]) == [node_x, node_x, node_y]
  assert contract_arbitrary_sum_node_group([node_x, additive_invert(node_x), node_y]) == [node_y]
  assert contract_arbitrary_sum_node_group([node_1, node_x,
                                            additive_invert(node_x), node_y]) == [node_1, node_y]
  assert contract_arbitrary_sum_node_group([
      node_1, node_x, additive_invert(node_x),
      additive_invert(node_x), node_y
      ]) == [node_y, node_not_x]
  assert contract_arbitrary_sum_node_group([
      node_1, node_x,
      additive_invert(node_x),
      additive_invert(node_x), node_x, node_y,
      additive_invert(node_x_and_y)
      ]) == [node_y, Node(prob_x_and_y.invert())]
  assert contract_arbitrary_sum_node_group([node_1, node_x, node_y,
                                            additive_invert(node_x_and_y)]
                                           ) == [node_x_and_y, node_1]
