from typing import List
from probnode.computation.node import *
from probnode.probability.event import SureEvent
from probnode.probability.probability import *
from probnode.P import P


def contract_prob_exp_node_group(group_node: List[Node]) -> List[Node]:
  if len(group_node.args) == 2:
    return contract_2_nodes(group_node)
  elif len(group_node.args) == 3:
    return contract_3_nodes(group_node)
  return group_node


def contract_2_nodes(group_node: ChainNode):
  if type(group_node) is SumNode:
    return contract_sum_2_nodes(group_node)
  if type(group_node) is ProductNode:
    return contract_product_2_nodes(group_node)


def contract_3_nodes(group_node: ChainNode):
  if type(group_node) is SumNode:
    return contract_product_2_nodes(group_node)
  if type(group_node) is ProductNode:
    return contract_product_3_nodes(group_node)


def contract_sum_2_nodes(sum_nodes: SumNode):
  node1 = sum_nodes.args[0]
  node2 = sum_nodes.args[1]
  if type(node1.exp) is SureEvent and issubclass(type(node2), AdditiveInverse):
    return [Node(node2.exp.invert())]
  if node1 in [AdditiveInverseNode.from_node(node2), AdditiveInverseChainNode.from_node(node2)]:
    return []


def contract_sum_3_nodes(sum_nodes: SumNode):
  pass


def contract_product_2_nodes(sum_nodes: SumNode):
  pass


def contract_product_3_nodes(sum_nodes: SumNode):
  pass