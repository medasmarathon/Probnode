from probnode.computation.node import *
from probnode.computation.probabilityContractingLogic import *
from probnode.probability.event import SureEvent
from probnode.probability.probability import *
from probnode.P import P
from typing import List
import pytest


@pytest.mark.parametrize(("input", "expect"), [([], EmptyNode())])
def test_contract_sum_2_nodes(input: List[Node], expect: Node):
  assert contract_sum_2_nodes(input) == expect