from typing import List, Type, Union
from probnode.computation.node import *
from probnode.probability.event import SureEvent
from probnode.probability.probability import *
from probnode.P import P


def contract_prob_exp_node_group(
    chain_type: Union[Type[SumNode], Type[ProductNode]], node_list: List[Node]
    ) -> ChainNode:
  if len(node_list) == 2:
    return contract_2_nodes(chain_type, node_list)
  elif len(node_list) == 3:
    return contract_3_nodes(chain_type, node_list)
  return node_list


def contract_2_nodes(chain_type: Union[Type[SumNode], Type[ProductNode]], node_list: List[Node]):
  if chain_type is SumNode:
    return contract_sum_2_nodes(node_list)
  if chain_type is ProductNode:
    return contract_product_2_nodes(node_list)


def contract_3_nodes(chain_type: Union[Type[SumNode], Type[ProductNode]], node_list: List[Node]):
  if chain_type is SumNode:
    return contract_product_2_nodes(node_list)
  if chain_type is ProductNode:
    return contract_product_3_nodes(node_list)


def contract_sum_2_nodes(sum_nodes: List[Node]) -> Union[Node, None]:
  if len(sum_nodes) == 0:
    return None
  node1 = sum_nodes[0]
  node2 = sum_nodes[1]
  if type(node1.exp) is SureEvent and issubclass(type(node2), AdditiveInverse):
    return Node(node2.exp.invert())
  if node1 in [AdditiveInverseNode.from_node(node2), AdditiveInverseChainNode.from_node(node2)]:
    return None


def contract_sum_3_nodes(sum_nodes: SumNode):
  pass


def contract_product_2_nodes(sum_nodes: SumNode):
  pass


def contract_product_3_nodes(sum_nodes: SumNode):
  pass