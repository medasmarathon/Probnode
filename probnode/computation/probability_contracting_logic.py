from typing import List, Type, Union
from probnode.core.node import *
from probnode.probability.event import SureEvent
from probnode.probability.probability import *
from probnode import P


def contract_pattern_node_group(
    chain_type: Union[Type[SumNode], Type[ProductNode]], node_list: List[Node]
    ) -> List[Node]:
  if len(node_list) == 2:
    result = contract_2_nodes(chain_type, node_list)
  elif len(node_list) == 3 and chain_type is SumNode:
    result = contract_sum_3_nodes(node_list)

  if result is not None:
    return result
  return node_list


def contract_2_nodes(chain_type: Union[Type[SumNode], Type[ProductNode]],
                     node_list: List[Node]) -> Union[Node, None]:
  if chain_type is SumNode:
    return try_contract_sum_2_nodes(node_list)
  if chain_type is ProductNode:
    return contract_product_2_nodes(node_list)


def try_contract_sum_2_nodes(sum_nodes: List[Node]) -> Union[Node, None]:
  if len(sum_nodes) != 2:
    raise ValueError("List parameter must have 2 nodes")
  node1 = sum_nodes[0]
  node2 = sum_nodes[1]
  if is_complement_pattern(node1, node2):
    return Node(node2.exp.invert())
  if is_negating_pattern(node1, node2):
    return Node(None, 0)
  return None


def contract_sum_3_nodes(sum_nodes: List[Node]) -> Union[Node, None]:
  if len(sum_nodes) != 3:
    raise ValueError("List parameter must have 3 nodes")
  result = try_contract_or_probability_pattern(sum_nodes[0], sum_nodes[1], sum_nodes[2])
  if result is not None:
    return result


def contract_product_2_nodes(product_nodes: List[Node]) -> Union[Node, None]:
  if len(product_nodes) != 2:
    raise ValueError("List parameter must have 2 nodes")
  node1 = product_nodes[0]
  node2 = product_nodes[1]
  if is_reciprocal_pattern(node1, node2):     # P(A) / P(A) = 1
    return Node(None, 1)

  conditional_probnode = try_contract_conditional_probability_pattern(
      node1, node2
      )     # P(A ^ B) / P(B) = P(A | B)
  if conditional_probnode is not None:
    return conditional_probnode

  if node1.exp is not None and node2.exp is not None:     # default is joint probability: P(A)P(B) = P(A ^ B)
    return Node(P(node1.exp & node2.exp))
  return None


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


def is_conditional_probability_pattern(
    node_A_and_B: Node, reciprocal_node_B: Node
    ) -> bool:     # P(A ^ B) / P(B)
  if node_A_and_B.exp is None or (not issubclass(type(reciprocal_node_B), Reciprocal)):
    return False
  A_and_B_exp = node_A_and_B.exp
  B_exp = reciprocal_node_B.reciprocate().exp
  if type(A_and_B_exp) is AndProbabilityExpression and B_exp in [A_and_B_exp.base_exp,
                                                                 A_and_B_exp.aux_exp]:
    return True
  return False


def try_contract_conditional_probability_pattern(
    node_A_and_B: Node, reciprocal_node_B: Node
    ) -> Union[Node, None]:     # P(A ^ B) / P(B)
  if node_A_and_B.exp is None or (not issubclass(type(reciprocal_node_B), Reciprocal)):
    return None
  A_and_B_exp = node_A_and_B.exp
  B_exp = reciprocal_node_B.reciprocate().exp
  if type(A_and_B_exp) is AndProbabilityExpression and (B_exp in [A_and_B_exp.base_exp,
                                                                  A_and_B_exp.aux_exp]):
    numerator_exps = [A_and_B_exp.base_exp, A_and_B_exp.aux_exp]
    A_exp = list(filter(lambda x: x != B_exp, numerator_exps)).pop()
    return Node(P(A_exp // B_exp))
  return None


def is_or_probability_pattern(
    node1: Node, node2: Node, node3: Node
    ) -> bool:     # P(A) + P(B) - P(A ^ B) = P(A v B)
  for node in [node1, node2, node3]:
    additive_invert_node = node.additive_invert()
    if type(additive_invert_node.exp) is AndProbabilityExpression:
      other_nodes = list(filter(lambda x: x != node, [node1, node2, node3]))
      other_exps = map(lambda x: x.exp if x.exp is not None else None, other_nodes)
      if set(other_exps) == set([additive_invert_node.exp.aux_exp,
                                 additive_invert_node.exp.base_exp]):
        return True
  return False


def try_contract_or_probability_pattern(node1: Node, node2: Node, node3: Node) -> Union[Node, None]:
  for node in [node1, node2, node3]:
    additive_invert_node = node.additive_invert()
    if type(additive_invert_node.exp) is AndProbabilityExpression:
      other_nodes = list(filter(lambda x: x != node, [node1, node2, node3]))
      other_exps = map(lambda x: x.exp if x.exp is not None else None, other_nodes)
      if set(other_exps) == set([additive_invert_node.exp.aux_exp,
                                 additive_invert_node.exp.base_exp]):
        return Node(additive_invert_node.exp.base_exp | additive_invert_node.exp.aux_exp)
  return None