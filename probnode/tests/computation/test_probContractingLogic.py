from probnode.computation.node import *
from probnode.computation.probabilityContractingLogic import *
from probnode.probability.event import *
from probnode.probability.probability import *
from probnode import *
from typing import List
import pytest


@pytest.mark.parametrize(
    ("input", "expect"),
    [([N(P(Event("sample"))), AdditiveInverseNode(P(Event("sample")))], Node()),
     ([
         N(P(Event("sample1"))) + N(P(Event("sample2"))),
         AdditiveInverseChainNode.from_node(N(P(Event("sample1"))) + N(P(Event("sample2"))))
         ], Node())]
    )
def test_contract_sum_2_nodes(input: List[Node], expect: Node):
  assert contract_sum_2_nodes(input) == expect


@pytest.mark.parametrize(
    ("input", "expect"),
    [([N(P(Event("sample"))), ReciprocalNode(P(Event("sample")))], Node(None, 1)),
     ([
         N(P(Event("sample1")) & P(Event("sample2"))),
         ReciprocalNode.from_node(N(P(Event("sample2"))))
         ], N(P(Event("sample1")) // P(Event("sample2"))))]
    )
def test_contract_product_2_nodes(input: List[Node], expect: Node):
  assert contract_product_2_nodes(input) == expect
