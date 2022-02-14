from typing import List, Type, Union
from probnode.computation.node import *
from probnode.probability.event import SureEvent
from probnode.probability.probability import *
from probnode.P import P


def contract_pattern_node_group(
    chain_type: Union[Type[SumNode], Type[ProductNode]], node_list: List[Node]
    ) -> ChainNode:
  if len(node_list) == 2:
    return contract_2_nodes(chain_type, node_list)
  elif len(node_list) == 3 and chain_type is SumNode:
    return contract_sum_3_nodes(node_list)
  return node_list


def contract_2_nodes(chain_type: Union[Type[SumNode], Type[ProductNode]], node_list: List[Node]):
  if chain_type is SumNode:
    return contract_sum_2_nodes(node_list)
  if chain_type is ProductNode:
    return contract_product_2_nodes(node_list)


def contract_sum_2_nodes(sum_nodes: List[Node]) -> Union[Node, None]:
  if len(sum_nodes) != 2:
    raise ValueError("List parameter must have 2 nodes")
  node1 = sum_nodes[0]
  node2 = sum_nodes[1]
  if is_complement_pattern(node1, node2):
    return Node(node2.exp.invert())
  if is_negating_pattern(node1, node2):
    return Node(None, 0)


def contract_sum_3_nodes(sum_nodes: List[Node]):
  if len(sum_nodes) != 3:
    raise ValueError("List parameter must have 3 nodes")


def contract_product_2_nodes(product_nodes: List[Node]):
  if len(product_nodes) != 2:
    raise ValueError("List parameter must have 2 nodes")
  node1 = product_nodes[0]
  node2 = product_nodes[1]
  if is_reciprocal_pattern(node1, node2):     # P(A) / P(A) = 1
    return Node(None, 1)


def is_complement_pattern(sure_event: Node, event_node: Node) -> bool:
  if type(sure_event.exp) is SureEvent and issubclass(type(event_node),
                                                      AdditiveInverse):     # 1 - P(A) = P(not A)
    return True
  return False


def is_negating_pattern(event_node: Node, inverse_event_node: Node) -> bool:
  if event_node in [AdditiveInverseNode.from_node(inverse_event_node),
                    AdditiveInverseChainNode.from_node(inverse_event_node)]:     # P(A) vs - P(A)
    return True
  return False


def is_reciprocal_pattern(event_node: Node, reciprocal_event_node: Node) -> bool:
  if event_node in [ReciprocalNode.from_node(reciprocal_event_node),
                    ReciprocalChainNode.from_node(reciprocal_event_node)]:     # P(A) vs 1/ P(A)
    return True
  return False


def is_joint_probability_pattern(node_A_given_B: Node, node_B: Node):     # P(A | B) * P(B)
  return False


def is_independent_joint_probability_pattern(node_A: Node, node_B: Node):     # P(A) * P(B)
  return False


def is_conditional_probability_pattern(node_A_and_B: Node, node_B: Node):     # P(A ^ B) / P(B)
  return False