from probnode import *
from probnode.probability import *
from probnode.core.node import *
from probnode.computation.probability_contracting_logic import *
from typing import List
import pytest


@pytest.mark.parametrize(
    ("input", "expect"),
    [([N(P(Outcome("sample"))), AdditiveInverseNode(P(Outcome("sample")))], Node(None, 0)),
     ([
         N(P(Outcome("sample1"))) + N(P(Outcome("sample2"))),
         AdditiveInverseChainNode.from_node(N(P(Outcome("sample1"))) + N(P(Outcome("sample2"))))
         ], Node(None, 0))]
    )
def test_contract_sum_2_nodes(input: List[Node], expect: Node):
  assert try_contract_sum_2_nodes(input) == expect


@pytest.mark.parametrize(("input", "expect"), [
    ([N(P(Outcome("sample"))), ReciprocalNode(P(Outcome("sample")))], Node(None, 1)),
    ([
        N(P(Outcome("sample1")) & P(Outcome("sample2"))),
        ReciprocalNode.from_node(N(P(Outcome("sample2"))))
        ], N(P(Outcome("sample1")) // P(Outcome("sample2")))),
    ([N(P(Outcome("sample1"))), N(P(Outcome("sample2")))], N(P(Outcome("sample1")) & P(Outcome("sample2"))))
    ])
def test_contract_product_2_nodes(input: List[Node], expect: Node):
  assert contract_product_2_nodes(input) == expect


def test_is_or_probability_pattern():
  assert is_or_probability_pattern(
      N(P(Outcome("x"))), N(P(Outcome("y"))),
      N(P(Outcome("x")) & P(Outcome("y"))).additive_invert()
      ) == True
  assert is_or_probability_pattern(
      N(P(Outcome("x"))), N(P(Outcome("yyyy"))),
      N(P(Outcome("x")) & P(Outcome("y"))).additive_invert()
      ) == False
  assert is_or_probability_pattern(
      N(P(Outcome("x"))), N(P(Outcome("yyyy"))), N(P(Outcome("x")) & P(Outcome("y")))
      ) == False


def test_try_contract_or_probability_pattern():
  assert try_contract_or_probability_pattern(
      N(P(Outcome("x"))), N(P(Outcome("y"))),
      N(P(Outcome("x")) & P(Outcome("y"))).additive_invert()
      ) == N(P(Outcome("x")) | P(Outcome("y")))
  assert try_contract_or_probability_pattern(
      N(P(Outcome("x"))), N(P(Outcome("yyyy"))),
      N(P(Outcome("x")) & P(Outcome("y"))).additive_invert()
      ) == None
  assert try_contract_or_probability_pattern(
      N(P(Outcome("x"))), N(P(Outcome("yyyy"))), N(P(Outcome("x")) & P(Outcome("y")))
      ) == None


def test_contract_sum_3_nodes():
  assert contract_sum_3_nodes([
      N(P(Outcome("x"))),
      N(P(Outcome("y"))),
      N(P(Outcome("x")) & P(Outcome("y"))).additive_invert()
      ]) == N(P(Outcome("x")) | P(Outcome("y")))
  assert contract_sum_3_nodes([
      N(P(Outcome("x"))),
      N(P(Outcome("yyyy"))),
      N(P(Outcome("x")) & P(Outcome("y"))).additive_invert()
      ]) == None
  assert contract_sum_3_nodes([
      N(P(Outcome("x"))), N(P(Outcome("yyyy"))),
      N(P(Outcome("x")) & P(Outcome("y")))
      ]) == None
