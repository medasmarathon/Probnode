from collections import Counter
from typing import List, Tuple
import pytest
from probnode import *
from probnode.computation.contract import *


def test_contract():
  sure_prob = ES(GenericSureEventSet())
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  prob_y_and_x = ES(prob_y & prob_x)
  prob_x_or_y = ES(prob_x | prob_y)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  node_y_and_x = ProbabilityMeasure(prob_y_and_x)
  node_y_when_x = p__X(ES(prob_y // prob_x))
  node_x_when_y = p__X(ES(prob_x // prob_y))

  chain_1 = p__X(prob_x) + p__X(prob_y) - p__X(prob_x_and_y)
  chain_2 = chain_1 + p__X(sure_prob)
  chain_3 = p__X(prob_x) - p__X(prob_x_and_y) + p__X(prob_y)
  chain_4 = p__X(prob_x) - p__X(prob_x_and_y) + p__X(prob_y) * p__X(prob_z) + p__X(prob_y)
  chain_5 = p__X(prob_x) - p__X(prob_x_and_y) + p__X(prob_y) * p__X(prob_z) + p__X(prob_y
                                                                                   ) - p__X(prob_y)
  chain_6 = p__X(prob_x) - p__X(prob_x_and_y) + p__X(prob_y) * p__X(prob_z) + p__X(prob_y) - p__X(
      prob_y
      ) + p__X(prob_x) * p__X(prob_y) * node_y_when_x

  assert contract(SumP()) == SumP()
  assert contract(chain_1) == p__X(prob_x_or_y)
  assert contract(chain_2) == (p__X(sure_prob) + p__X(prob_x_or_y))
  assert contract(chain_3) == p__X(prob_x_or_y)
  assert contract(chain_4) == p__X(prob_y) * p__X(prob_z) + p__X(prob_x_or_y)
  assert contract(chain_5) == p__X(prob_y) * p__X(prob_z) + p__X(prob_x) - p__X(prob_x_and_y)
  assert contract(chain_6).is_permutation_of(
      p__X(prob_y) * p__X(prob_z) + p__X(prob_x) - p__X(prob_x_and_y) + p__X(prob_y) * node_y_and_x
      )


def test_replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs():
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  prob_x_or_y = ES(prob_x | prob_y)
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([], []) == ([], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x], []) == ([prob_x], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([], [prob_x_and_y]) == ([], [
      prob_x_and_y
      ])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x], [prob_x_and_y]) == ([
      prob_x
      ], [prob_x_and_y])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x, prob_y],
                                                                    [prob_x_and_y]) == ([
                                                                        prob_x_or_y
                                                                        ], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x, prob_y, prob_z],
                                                                    [prob_x_and_y]) == ([
                                                                        prob_z, prob_x_or_y
                                                                        ], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x, prob_z, prob_y],
                                                                    [prob_x_and_y]) == ([
                                                                        prob_z, prob_x_or_y
                                                                        ], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x, prob_y, prob_y],
                                                                    [prob_x_and_y]) == ([
                                                                        prob_y, prob_x_or_y
                                                                        ], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x, prob_x, prob_y],
                                                                    [prob_x_and_y]) == ([
                                                                        prob_x, prob_x_or_y
                                                                        ], [])


def test_remove_or_prob_pattern_nodes_from_classified_lists():
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  node_x = ProbabilityMeasure(prob_x)
  node_y = ProbabilityMeasure(prob_y)
  node_z = ProbabilityMeasure(prob_z)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  node_x_or_y = ProbabilityMeasure(ES(prob_x | prob_y))
  inverted_node_x_and_y = node_x_and_y.additive_invert()
  assert remove_or_prob_pattern_nodes_from_classified_lists([], []) == ([], [])
  assert remove_or_prob_pattern_nodes_from_classified_lists([node_x], []) == ([node_x], [])
  assert remove_or_prob_pattern_nodes_from_classified_lists([], [inverted_node_x_and_y]) == ([], [
      inverted_node_x_and_y
      ])
  assert remove_or_prob_pattern_nodes_from_classified_lists([node_x], [inverted_node_x_and_y]) == ([
      node_x
      ], [inverted_node_x_and_y])
  assert remove_or_prob_pattern_nodes_from_classified_lists([node_x, node_y],
                                                            [inverted_node_x_and_y]) == ([
                                                                node_x_or_y
                                                                ], [])
  assert remove_or_prob_pattern_nodes_from_classified_lists([node_x, node_y, node_z],
                                                            [inverted_node_x_and_y]) == ([
                                                                node_z, node_x_or_y
                                                                ], [])
  assert remove_or_prob_pattern_nodes_from_classified_lists([node_x, node_z, node_y],
                                                            [inverted_node_x_and_y]) == ([
                                                                node_z, node_x_or_y
                                                                ], [])
  assert remove_or_prob_pattern_nodes_from_classified_lists([node_x, node_y, node_y],
                                                            [inverted_node_x_and_y]) == ([
                                                                node_y, node_x_or_y
                                                                ], [])
  assert remove_or_prob_pattern_nodes_from_classified_lists([node_x, node_x, node_y],
                                                            [inverted_node_x_and_y]) == ([
                                                                node_x, node_x_or_y
                                                                ], [])


def test_remove_negating_nodes_from_classified_lists():
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  node_x = ProbabilityMeasure(prob_x)
  node_y = ProbabilityMeasure(prob_y)
  node_z = ProbabilityMeasure(prob_z)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  inverted_node_x_and_y = node_x_and_y.additive_invert()
  inverted_node_x = node_x.additive_invert()
  inverted_node_y = node_y.additive_invert()
  assert remove_negating_nodes_from_classified_lists([], []) == ([], [])
  assert remove_negating_nodes_from_classified_lists([node_x_and_y],
                                                     [inverted_node_x_and_y]) == ([], [])
  assert remove_negating_nodes_from_classified_lists([], [inverted_node_x_and_y]) == ([], [
      inverted_node_x_and_y
      ])
  assert remove_negating_nodes_from_classified_lists([node_x, node_x_and_y],
                                                     [inverted_node_x_and_y]) == ([node_x], [])
  assert remove_negating_nodes_from_classified_lists([node_x, node_x], []) == ([node_x, node_x], [])
  assert remove_negating_nodes_from_classified_lists([node_x, node_x, node_y],
                                                     [inverted_node_x]) == ([node_x, node_y], [])
  assert remove_negating_nodes_from_classified_lists([node_x, node_x, node_y],
                                                     [inverted_node_x, inverted_node_y]) == ([
                                                         node_x
                                                         ], [])
  assert remove_negating_nodes_from_classified_lists([node_y],
                                                     [inverted_node_x, inverted_node_y]) == ([], [
                                                         inverted_node_x
                                                         ])


def test_contract_complement_nodes():
  sure_prob = ES(GenericSureEventSet())
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  node_1 = ProbabilityMeasure(sure_prob)
  node_x = ProbabilityMeasure(prob_x)
  node_y = ProbabilityMeasure(prob_y)
  node_z = ProbabilityMeasure(prob_z)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  node_not_x = ProbabilityMeasure(prob_x.invert())
  node_not_y = ProbabilityMeasure(prob_y.invert())
  node_not_x_and_y = ProbabilityMeasure(prob_x_and_y.invert())

  sum = SumP()
  sum.args = [2]
  assert contract_complement_nodes(sum).args == [2]

  assert contract_complement_nodes(node_x + node_y).args == [node_x, node_y]
  assert contract_complement_nodes(node_1 - node_y).args == [node_not_y]
  assert contract_complement_nodes(2 + node_x + node_y + node_1).args == [3, node_x, node_y]
  assert contract_complement_nodes(2 + node_x - node_not_y).args == [1, node_x, node_y]
  assert contract_complement_nodes(1 + node_1 - node_not_y -
                                   node_not_x_and_y).args == [node_y, node_x_and_y]


def test_contract_negating_nodes():
  sure_prob = ES(GenericSureEventSet())
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  node_1 = ProbabilityMeasure(sure_prob)
  node_x = ProbabilityMeasure(prob_x)
  node_y = ProbabilityMeasure(prob_y)
  node_z = ProbabilityMeasure(prob_z)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  node_not_x = ProbabilityMeasure(prob_x.invert())
  node_not_y = ProbabilityMeasure(prob_y.invert())
  node_not_x_and_y = ProbabilityMeasure(prob_x_and_y.invert())

  sum = SumP()
  sum.args = [2]
  assert contract_negating_nodes(sum).args == [2]

  assert contract_negating_nodes(node_x + node_y).args == [node_x, node_y]
  assert contract_negating_nodes(node_y - node_y).args == []
  assert contract_negating_nodes(2 + node_x + node_y + node_1).args == [3, node_x, node_y]
  assert contract_negating_nodes(2 + node_x - node_1).args == [1, node_x]
  assert contract_negating_nodes(1 + node_x_and_y - node_y - node_x_and_y).args == [1, -node_y]


def test_remove_complement_nodes_from_classified_lists():
  sure_prob = ES(GenericSureEventSet())
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  node_1 = ProbabilityMeasure(sure_prob)
  node_x = ProbabilityMeasure(prob_x)
  node_y = ProbabilityMeasure(prob_y)
  node_z = ProbabilityMeasure(prob_z)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  node_not_x = ProbabilityMeasure(prob_x.invert())
  node_not_y = ProbabilityMeasure(prob_y.invert())
  node_not_x_and_y = ProbabilityMeasure(prob_x_and_y.invert())
  assert remove_complement_nodes_from_classified_lists(2, [], []) == (2, [], [])
  assert remove_complement_nodes_from_classified_lists(2, [node_x, node_y, node_1],
                                                       []) == (2, [node_x, node_y, node_1], [])
  assert remove_complement_nodes_from_classified_lists(2, [node_x],
                                                       [node_not_y]) == (2, [node_x], [node_not_y])
  assert remove_complement_nodes_from_classified_lists(2, [node_y],
                                                       [node_not_y]) == (2, [node_y], [node_not_y])
  assert remove_complement_nodes_from_classified_lists(2, [node_1],
                                                       [node_not_y.additive_invert()
                                                        ]) == (1, [node_1, node_y], [])
  assert remove_complement_nodes_from_classified_lists(
      2, [node_1, node_1], [node_not_y.additive_invert()]
      ) == (1, [node_1, node_1, node_y], [])
  assert remove_complement_nodes_from_classified_lists(
      2, [node_1, node_1, node_1],
      [node_x.additive_invert(), node_y.additive_invert()]
      ) == (0, [node_1, node_1, node_1, node_not_x, node_not_y], [])
  assert remove_complement_nodes_from_classified_lists(
      2, [node_1],
      [node_x.additive_invert(), node_x_and_y.additive_invert()]
      ) == (0, [node_1, node_not_x, node_not_x_and_y], [])
  assert remove_complement_nodes_from_classified_lists(
      2, [node_1],
      [node_x.additive_invert(), node_x_and_y.additive_invert(), node_z]
      ) == (0, [node_1, node_not_x, node_not_x_and_y], [node_z])


def test_contract_arbitrary_sum_node_group():
  sure_prob = ES(GenericSureEventSet())
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  prob_x_or_y = ES(prob_x | prob_y)
  node_1 = ProbabilityMeasure(sure_prob)
  node_x = ProbabilityMeasure(prob_x)
  node_y = ProbabilityMeasure(prob_y)
  node_z = ProbabilityMeasure(prob_z)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  node_not_x = ProbabilityMeasure(prob_x.invert())
  node_not_y = ProbabilityMeasure(prob_y.invert())
  node_x_or_y = ProbabilityMeasure(prob_x_or_y)

  assert contract_arbitrary_sum_node_group([]) == []
  assert contract_arbitrary_sum_node_group([node_x]) == [node_x]
  assert contract_arbitrary_sum_node_group([node_x, node_x, node_y]) == [node_x, node_x, node_y]
  assert contract_arbitrary_sum_node_group([node_x, node_x.additive_invert(), node_y]) == [node_y]
  assert contract_arbitrary_sum_node_group([node_1, node_x,
                                            node_x.additive_invert(), node_y]) == [1.0, node_y]
  assert contract_arbitrary_sum_node_group([
      node_1, node_x, node_x.additive_invert(),
      node_x.additive_invert(), node_y
      ]) == [node_y, node_not_x]
  assert contract_arbitrary_sum_node_group([
      node_1, node_x,
      node_x.additive_invert(),
      node_x.additive_invert(), node_x, node_y,
      node_x_and_y.additive_invert()
      ]) == [node_y, ProbabilityMeasure(prob_x_and_y.invert())]
  assert contract_arbitrary_sum_node_group([node_1, node_x, node_y,
                                            node_x_and_y.additive_invert()]) == [1.0, node_x_or_y]
  assert contract_arbitrary_sum_node_group([
      node_1, node_x, node_y, node_not_y,
      node_x_and_y.additive_invert()
      ]) == [1.0, node_not_y, node_x_or_y]
  assert contract_arbitrary_sum_node_group([
      node_1, node_x, node_y,
      node_not_y.additive_invert(),
      node_x_and_y.additive_invert()
      ]) == [node_x_or_y, node_y]


def test_replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs():
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  prob_y_when_x = ES(prob_y // prob_x)
  prob_x_when_y = ES(prob_x // prob_y)
  assert replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs([], []) == ([], [])
  assert replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs([prob_x],
                                                                            []) == ([prob_x], [])
  assert replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs([],
                                                                            [prob_x_and_y
                                                                             ]) == ([],
                                                                                    [prob_x_and_y])
  assert replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs([prob_x],
                                                                            [prob_x_and_y
                                                                             ]) == ([],
                                                                                    [prob_y_when_x])
  assert replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs([prob_x, prob_y],
                                                                            [prob_x_and_y]) == ([
                                                                                prob_y
                                                                                ], [prob_y_when_x])
  assert replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs([
      prob_x, prob_y, prob_z
      ], [prob_x_and_y]) == ([prob_y, prob_z], [prob_y_when_x])
  assert replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs([
      prob_y, prob_z, prob_x
      ], [prob_x_and_y]) == ([prob_z, prob_x], [prob_x_when_y])
  assert replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs([
      prob_x, prob_y, prob_y
      ], [prob_x_and_y]) == ([prob_y, prob_y], [prob_y_when_x])
  assert replace_reciprocal_probs_vs_and_probs_lists_with_conditional_probs([
      prob_x, prob_x, prob_y
      ], [prob_x_and_y]) == ([prob_x, prob_y], [prob_y_when_x])


def test_simplify_conditional_pattern_nodes_from_classified_lists():
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  node_x = p__X(prob_x)
  node_y = p__X(prob_y)
  node_z = p__X(prob_z)
  node_x_and_y = p__X(ES(prob_x & prob_y))
  node_y_when_x = p__X(ES(prob_y // prob_x))
  node_x_when_y = p__X(ES(prob_x // prob_y))
  assert simplify_conditional_pattern_nodes_from_classified_lists([], []) == ([], [])
  assert simplify_conditional_pattern_nodes_from_classified_lists([node_x], []) == ([node_x], [])
  assert simplify_conditional_pattern_nodes_from_classified_lists([], [node_x_when_y]) == ([], [
      node_x_when_y
      ])
  assert simplify_conditional_pattern_nodes_from_classified_lists([node_x_and_y],
                                                                  [node_x.reciprocate()]) == ([
                                                                      node_y_when_x
                                                                      ], [])
  assert simplify_conditional_pattern_nodes_from_classified_lists([node_x_and_y], [
      node_x.reciprocate(), node_y.reciprocate()
      ]) == ([node_y_when_x], [node_y.reciprocate()])
  assert simplify_conditional_pattern_nodes_from_classified_lists([node_x_and_y], [
      node_x.reciprocate(), node_y.reciprocate(),
      node_z.reciprocate()
      ]) == ([node_y_when_x], [node_y.reciprocate(), node_z.reciprocate()])
  assert simplify_conditional_pattern_nodes_from_classified_lists([node_x_and_y], [
      node_y.reciprocate(), node_x.reciprocate(),
      node_z.reciprocate()
      ]) == ([node_x_when_y], [node_x.reciprocate(), node_z.reciprocate()])
  assert simplify_conditional_pattern_nodes_from_classified_lists([node_x_and_y], [
      node_x.reciprocate(), node_y.reciprocate(),
      node_y.reciprocate()
      ]) == ([node_y_when_x], [node_y.reciprocate(), node_y.reciprocate()])
  assert simplify_conditional_pattern_nodes_from_classified_lists([node_x_and_y], [
      node_x.reciprocate(), node_x.reciprocate(),
      node_y.reciprocate()
      ]) == ([node_y_when_x], [node_x.reciprocate(), node_y.reciprocate()])


def test_contract_arbitrary_product_node_group():
  sure_prob = ES(GenericSureEventSet())
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  prob_y_and_x = ES(prob_y & prob_x)
  prob_x_or_y = ES(prob_x | prob_y)
  node_1 = ProbabilityMeasure(sure_prob)
  node_x = ProbabilityMeasure(prob_x)
  node_y = ProbabilityMeasure(prob_y)
  node_z = ProbabilityMeasure(prob_z)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  node_y_and_x = ProbabilityMeasure(prob_y_and_x)
  node_y_when_x = p__X(ES(prob_y // prob_x))
  node_x_when_y = p__X(ES(prob_x // prob_y))

  assert contract_arbitrary_product_node_group([]) == []
  assert contract_arbitrary_product_node_group([node_x]) == [node_x]
  assert contract_arbitrary_product_node_group([node_x, node_x, node_y]) == [node_x, node_x, node_y]
  assert contract_arbitrary_product_node_group([node_x, node_x.reciprocate(), node_y]) == [node_y]
  assert contract_arbitrary_product_node_group([node_1, node_x,
                                                node_x.reciprocate(), node_y]) == [node_y]
  assert contract_arbitrary_product_node_group([
      node_1, node_x, node_x.reciprocate(),
      node_x.reciprocate(), node_y
      ]) == [node_y, node_x.reciprocate()]
  assert contract_arbitrary_product_node_group([
      node_1, node_x,
      node_x.reciprocate(),
      node_x.reciprocate(), node_x, node_y, node_x_and_y
      ]) == [node_y, node_x_and_y]
  assert contract_arbitrary_product_node_group([node_1, node_x,
                                                node_y.reciprocate(),
                                                node_x_and_y]) == [node_x, node_x_when_y]
  assert contract_arbitrary_product_node_group([node_x, node_x,
                                                node_y_when_x]) == [node_x, node_y_and_x]
  assert contract_arbitrary_product_node_group([node_y, node_x, node_y_when_x,
                                                node_x_when_y]) == [node_y_and_x, node_x_and_y]


def test_contract_reciprocated_nodes():
  sure_prob = ES(GenericSureEventSet())
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  node_1 = ProbabilityMeasure(sure_prob)
  node_x = ProbabilityMeasure(prob_x)
  node_y = ProbabilityMeasure(prob_y)
  node_z = ProbabilityMeasure(prob_z)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  node_not_x = ProbabilityMeasure(prob_x.invert())
  node_not_y = ProbabilityMeasure(prob_y.invert())
  node_not_x_and_y = ProbabilityMeasure(prob_x_and_y.invert())

  sum = ProductP()
  sum.args = [2]
  assert contract_reciprocated_nodes(sum).args == [2]

  assert contract_reciprocated_nodes(node_x * node_y).args == [node_x, node_y]
  assert contract_reciprocated_nodes(node_y / node_y).args == []
  assert contract_reciprocated_nodes(2 * node_x / node_y * node_1
                                     ).args == [2, node_x, node_y.reciprocate()]
  assert contract_reciprocated_nodes(node_x_and_y * node_x / node_x_and_y / 0.5).args == [2, node_x]


def test_contract_conditional_pattern_nodes():
  sure_prob = ES(GenericSureEventSet())
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  prob_x_when_y = ES(prob_x // prob_y)
  node_1 = ProbabilityMeasure(sure_prob)
  node_x = ProbabilityMeasure(prob_x)
  node_y = ProbabilityMeasure(prob_y)
  node_z = ProbabilityMeasure(prob_z)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  node_x_when_y = ProbabilityMeasure(prob_x_when_y)
  node_not_x = ProbabilityMeasure(prob_x.invert())
  node_not_y = ProbabilityMeasure(prob_y.invert())
  node_not_x_and_y = ProbabilityMeasure(prob_x_and_y.invert())

  sum = ProductP()
  sum.args = [2]
  assert contract_conditional_pattern_nodes(sum).args == [2.0]

  assert contract_conditional_pattern_nodes(node_x * node_y).args == [node_x, node_y]
  assert contract_conditional_pattern_nodes(node_x_and_y / node_y).args == [node_x_when_y]
  assert contract_conditional_pattern_nodes(2 * node_x / node_y * node_1
                                            ).args == [2, node_x, node_y.reciprocate()]
  assert contract_conditional_pattern_nodes(node_x_and_y / node_y / 0.5).args == [2, node_x_when_y]


def test_contract_expanded_and_prob_pattern_nodes():
  sure_prob = ES(GenericSureEventSet())
  prob_x = ES(Outcome("x"))
  prob_y = ES(Outcome("y"))
  prob_z = ES(Outcome("z"))
  prob_x_and_y = ES(prob_x & prob_y)
  prob_x_when_y = ES(prob_x // prob_y)
  node_1 = ProbabilityMeasure(sure_prob)
  node_x = ProbabilityMeasure(prob_x)
  node_y = ProbabilityMeasure(prob_y)
  node_z = ProbabilityMeasure(prob_z)
  node_x_and_y = ProbabilityMeasure(prob_x_and_y)
  node_x_when_y = ProbabilityMeasure(prob_x_when_y)
  node_not_x = ProbabilityMeasure(prob_x.invert())
  node_not_y = ProbabilityMeasure(prob_y.invert())
  node_not_x_and_y = ProbabilityMeasure(prob_x_and_y.invert())

  sum = ProductP()
  sum.args = [2]
  assert contract_expanded_and_prob_pattern_nodes(sum).args == [2.0]

  assert contract_expanded_and_prob_pattern_nodes(node_x * node_y).args == [node_x, node_y]
  assert contract_expanded_and_prob_pattern_nodes(node_x_and_y / node_y
                                                  ).args == [node_x_and_y,
                                                             node_y.reciprocate()]
  assert contract_expanded_and_prob_pattern_nodes(node_x_when_y * node_y).args == [node_x_and_y]
  assert contract_expanded_and_prob_pattern_nodes(2 * node_x_when_y / node_y * node_y).args == [
      2.0, node_x_and_y, node_y.reciprocate()
      ]
