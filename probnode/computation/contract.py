from typing import Tuple, Type, Union
from probnode import SureEvent
from probnode.computation.node import *
from probnode.computation.nodeLogic import additive_invert, is_pure_node
from probnode.probability import *


def contract(chain: ChainNode) -> Node:
  if not issubclass(type(chain), ChainNode):
    raise TypeError(f"Chain argument must be subclass of type {ChainNode.__name__}")

  return contract_arbitrary_node_group(type(chain), chain.args)


def contract_arbitrary_node_group(
    chain_type: Union[Type[SumNode], Type[ProductNode]], node_list: List[Node]
    ) -> List[Node]:
  if chain_type is SumNode:
    contract_arbitrary_sum_node_group(node_list)
  if chain_type is ProductNode:
    contract_arbitrary_product_node_group(node_list)


def contract_arbitrary_sum_node_group(node_list: List[Node]) -> List[Node]:
  (normal_additive_nodes, additive_inverse_nodes) = split_normal_vs_inverse_nodes(node_list)
  if len(additive_inverse_nodes) == 0 or len(normal_additive_nodes) == 0:
    return node_list

  (normal_additive_nodes,
   additive_inverse_nodes) = contract_negating_nodes(normal_additive_nodes, additive_inverse_nodes)
  if len(additive_inverse_nodes) == 0 or len(normal_additive_nodes) == 0:
    return additive_inverse_nodes + normal_additive_nodes

  (normal_additive_nodes, additive_inverse_nodes
   ) = contract_or_prob_pattern_nodes(normal_additive_nodes, additive_inverse_nodes)
  if len(additive_inverse_nodes) == 0:
    return normal_additive_nodes

  (normal_additive_nodes, additive_inverse_nodes
   ) = contract_complement_nodes(normal_additive_nodes, additive_inverse_nodes)
  return normal_additive_nodes + additive_inverse_nodes


def split_normal_vs_inverse_nodes(node_list: List[Node]) -> Tuple[List[Node], List[Node]]:
  additive_inverse_nodes = []
  normal_additive_nodes = []
  for node in node_list:
    if issubclass(type(node), AdditiveInverse):
      additive_inverse_nodes.append(node)
    else:
      normal_additive_nodes.append(node)
  return (normal_additive_nodes, additive_inverse_nodes)


def contract_negating_nodes(normal_additive_nodes: List[Node],
                            additive_inverse_nodes: List[Node]) -> Tuple[List[Node], List[Node]]:
  for inverse_node in additive_inverse_nodes[:]:     # P(A) - P(A) = 0
    for normal_node in normal_additive_nodes[:]:
      if additive_invert(
          inverse_node
          ) == normal_node and normal_node in normal_additive_nodes and inverse_node in additive_inverse_nodes:
        normal_additive_nodes.remove(normal_node)
        additive_inverse_nodes.remove(inverse_node)
  return (normal_additive_nodes, additive_inverse_nodes)


def contract_complement_nodes(
    normal_additive_nodes: List[Node], additive_inverse_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  for node in normal_additive_nodes[:]:     # 1 - P(A) = P(not A)
    if node == Node(P(SureEvent())) and len(additive_inverse_nodes) > 0:
      exp_node = additive_invert(additive_inverse_nodes[0])
      if is_pure_node(exp_node) and Node(P(SureEvent())) in normal_additive_nodes:
        normal_additive_nodes.remove(Node(P(SureEvent())))
        normal_additive_nodes.append(Node(exp_node.exp.invert()))
        additive_inverse_nodes.pop(0)
  return (normal_additive_nodes, additive_inverse_nodes)


def contract_or_prob_pattern_nodes(
    normal_additive_nodes: List[Node], additive_inverse_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  and_prob_list = []
  simple_prob_list = []
  for node in normal_additive_nodes[:]:
    if is_pure_node(node):
      simple_prob_list.append(node.exp)
      normal_additive_nodes.remove(node)
  for node in additive_inverse_nodes[:]:
    exp_node = additive_invert(node)
    if is_pure_node(exp_node):
      and_prob = exp_node.exp
      if type(and_prob) is AndProbabilityExpression and node in additive_inverse_nodes:
        and_prob_list.append(and_prob)
        additive_inverse_nodes.remove(node)
  (simple_prob_list,
   and_prob_list) = remove_same_exp_in_simple_vs_and_prob_lists(simple_prob_list, and_prob_list)
  normal_additive_nodes += list(map(lambda x: Node(x), simple_prob_list))
  additive_inverse_nodes += list(map(lambda x: additive_invert(Node(x)), and_prob_list))
  return (normal_additive_nodes, additive_inverse_nodes)


def remove_same_exp_in_simple_vs_and_prob_lists(
    simple_prob_list: List[BaseProbabilityExpression], and_prob_list: List[AndProbabilityExpression]
    ) -> Tuple[List[BaseProbabilityExpression], List[AndProbabilityExpression]]:
  and_exps_list = list(map(lambda x: [x.base_exp, x.aux_exp], and_prob_list))
  for simple_prob in simple_prob_list[:]:
    for idx, and_exps in enumerate(and_exps_list[:]):
      if simple_prob in and_exps:
        and_exps.remove(simple_prob)
        if len(and_exps) == 0:
          simple_prob_list.remove(and_prob_list[idx].aux_exp)
          simple_prob_list.remove(and_prob_list[idx].base_exp)
          simple_prob_list.append(and_prob_list[idx].base_exp | and_prob_list[idx].aux_exp)
          and_prob_list.pop(idx)
        break

  return (simple_prob_list, and_prob_list)


def contract_arbitrary_product_node_group(node_list: List[Node]) -> List[Node]:
  pass