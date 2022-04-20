from typing import Tuple, Type, Union
from probnode import SureEvent
from probnode.core import *
from probnode.probability import *


def contract(chain: ChainNode) -> ChainNode:
  if not issubclass(type(chain), ChainNode):
    raise TypeError(f"Chain argument must be subclass of type {ChainNode.__name__}")

  return contract_arbitrary_node_group(type(chain), chain.args)


def contract_arbitrary_node_group(
    chain_type: Union[Type[SumNode], Type[ProductNode]], node_list: List[Node]
    ) -> ChainNode:
  if chain_type is SumNode:
    result = SumNode()
    result.args = contract_arbitrary_sum_node_group(node_list)

  if chain_type is ProductNode:
    result = ProductNode()
    result.args = contract_arbitrary_product_node_group(node_list)
  return result if result is not None else None


def contract_arbitrary_sum_node_group(
    node_list: List[Union[float, Node]]
    ) -> List[Union[float, Node]]:
  node_list = _convert_SureEvent_in_node_list_to_float(node_list)
  (float_value, normal_additive_nodes,
   additive_inverse_nodes) = _split_float_vs_normal_vs_inverse_nodes(node_list)
  if _not_contractable(normal_additive_nodes, additive_inverse_nodes):
    return [
        float_value
        ] + normal_additive_nodes + additive_inverse_nodes if float_value != 0 else normal_additive_nodes + additive_inverse_nodes

  (normal_additive_nodes,
   additive_inverse_nodes) = contract_negating_nodes(normal_additive_nodes, additive_inverse_nodes)
  if _not_contractable(normal_additive_nodes, additive_inverse_nodes):
    return [
        float_value
        ] + normal_additive_nodes + additive_inverse_nodes if float_value != 0 else normal_additive_nodes + additive_inverse_nodes

  (normal_additive_nodes, additive_inverse_nodes
   ) = contract_or_prob_pattern_nodes(normal_additive_nodes, additive_inverse_nodes)
  if _not_contractable(normal_additive_nodes, additive_inverse_nodes):
    return [float_value] + normal_additive_nodes if float_value != 0 else normal_additive_nodes

  (float_value, normal_additive_nodes, additive_inverse_nodes
   ) = contract_complement_nodes(float_value, normal_additive_nodes, additive_inverse_nodes)

  if len(normal_additive_nodes) > 0:
    for idx, node in enumerate(normal_additive_nodes[:]):
      if issubclass(type(node), ChainNode):
        normal_additive_nodes[idx] = contract(node)
  if len(additive_inverse_nodes) > 0:
    for idx, node in enumerate(additive_inverse_nodes[:]):
      invert_node = node.additive_invert()
      if issubclass(type(invert_node), ChainNode):
        additive_inverse_nodes[idx] = contract(invert_node).additive_invert()
  return [
      float_value
      ] + normal_additive_nodes + additive_inverse_nodes if float_value != 0 else normal_additive_nodes + additive_inverse_nodes


def _not_contractable(
    normal_additive_nodes: List[Node], additive_inverse_nodes: List[Node]
    ) -> bool:
  return len(additive_inverse_nodes) == 0 or len(normal_additive_nodes) == 0


def _convert_SureEvent_in_node_list_to_float(
    node_list: List[Union[float, Node]]
    ) -> List[Union[float, Node]]:
  return list(map(lambda x: float(1) if x == Node(P(SureEvent())) else x, node_list))


def _split_float_vs_normal_vs_inverse_nodes(
    node_list: List[Union[float, Node]]
    ) -> Tuple[float, List[Node], List[Node]]:
  float_value = 0.0
  additive_inverse_nodes = []
  normal_additive_nodes = []
  for node in node_list:
    if isinstance(node, (int, float)):
      float_value = float_value + float(node)
    elif issubclass(type(node), AdditiveInverse):
      additive_inverse_nodes.append(node)
    else:
      normal_additive_nodes.append(node)
  return (float_value, normal_additive_nodes, additive_inverse_nodes)


def contract_negating_nodes(normal_additive_nodes: List[Node],
                            additive_inverse_nodes: List[Node]) -> Tuple[List[Node], List[Node]]:
  for inverse_node in additive_inverse_nodes[:]:     # P(A) - P(A) = 0
    for normal_node in normal_additive_nodes[:]:
      if inverse_node.additive_invert(
      ) == normal_node and normal_node in normal_additive_nodes and inverse_node in additive_inverse_nodes:
        normal_additive_nodes.remove(normal_node)
        additive_inverse_nodes.remove(inverse_node)
  return (normal_additive_nodes, additive_inverse_nodes)


def contract_complement_nodes(
    float_value: float, normal_additive_nodes: List[Node], additive_inverse_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  for node in additive_inverse_nodes[:]:
    if float_value >= 1:     # 1 - P(A) = P(not A)
      exp_node = node.additive_invert()
      if exp_node.is_pure_node():
        float_value = float_value - 1
        normal_additive_nodes.append(Node(exp_node.exp.invert()))
        additive_inverse_nodes.remove(node)
  return (float_value, normal_additive_nodes, additive_inverse_nodes)


def contract_or_prob_pattern_nodes(
    normal_additive_nodes: List[Node], additive_inverse_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  and_prob_list = []
  simple_prob_list = []
  for node in normal_additive_nodes[:]:
    if node.is_pure_node():
      simple_prob_list.append(node.exp)
      normal_additive_nodes.remove(node)
  for node in additive_inverse_nodes[:]:
    exp_node = node.additive_invert()
    if exp_node.is_pure_node():
      and_prob = exp_node.exp
      if type(and_prob) is AndProbabilityExpression and node in additive_inverse_nodes:
        and_prob_list.append(and_prob)
        additive_inverse_nodes.remove(node)
  (simple_prob_list, and_prob_list
   ) = replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs(simple_prob_list, and_prob_list)
  normal_additive_nodes += list(map(lambda x: Node(x), simple_prob_list))
  additive_inverse_nodes += list(map(lambda x: Node(x).additive_invert(), and_prob_list))
  return (normal_additive_nodes, additive_inverse_nodes)


def replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs(
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


def contract_arbitrary_product_node_group(
    node_list: List[Union[float, Node]]
    ) -> List[Union[float, Node]]:
  (float_value, normal_nodes,
   reciprocal_nodes) = split_float_vs_normal_vs_reciprocal_nodes(node_list)
  if len(reciprocal_nodes) == 0 or len(normal_nodes) == 0:
    return [float_value] + contract_expanded_and_prob_exp(
        normal_nodes + reciprocal_nodes
        ) if float_value != 1 else contract_expanded_and_prob_exp(normal_nodes + reciprocal_nodes)

  (normal_nodes, reciprocal_nodes) = contract_reciprocal_nodes(normal_nodes, reciprocal_nodes)
  if len(reciprocal_nodes) == 0 or len(normal_nodes) == 0:
    return [float_value] + reciprocal_nodes + contract_expanded_and_prob_exp(
        normal_nodes
        ) if float_value != 1 else reciprocal_nodes + contract_expanded_and_prob_exp(normal_nodes)

  (normal_nodes,
   reciprocal_nodes) = contract_conditional_pattern_nodes(normal_nodes, reciprocal_nodes)

  normal_nodes = contract_expanded_and_prob_exp(normal_nodes)

  if len(normal_nodes) > 0:
    for idx, node in enumerate(normal_nodes[:]):
      if issubclass(type(node), ChainNode):
        normal_nodes[idx] = contract(node)
  if len(reciprocal_nodes) > 0:
    for idx, node in enumerate(reciprocal_nodes[:]):
      invert_node = node.additive_invert()
      if issubclass(type(invert_node), ChainNode):
        reciprocal_nodes[idx] = contract(invert_node).additive_invert()
  return [
      float_value
      ] + normal_nodes + reciprocal_nodes if float_value != 1 else normal_nodes + reciprocal_nodes


def split_float_vs_normal_vs_reciprocal_nodes(
    node_list: List[Union[float, Node]]
    ) -> Tuple[float, List[Node], List[Node]]:
  float_value = 1.0
  reciprocal_nodes = []
  normal_nodes = []
  for node in node_list:
    if isinstance(node, (int, float)):
      float_value = float_value * float(node)
    elif issubclass(type(node), Reciprocal):
      reciprocal_nodes.append(node)
    else:
      normal_nodes.append(node)
  return (float_value, normal_nodes, reciprocal_nodes)


def contract_reciprocal_nodes(normal_nodes: List[Node],
                              reciprocal_nodes: List[Node]) -> Tuple[List[Node], List[Node]]:
  for reciproc_node in reciprocal_nodes[:]:     #  P(A) / P(A) = 1
    for normal_node in normal_nodes[:]:
      if reciproc_node.reciprocate(
      ) == normal_node and normal_node in normal_nodes and reciproc_node in reciprocal_nodes:
        normal_nodes.remove(normal_node)
        reciprocal_nodes.remove(reciproc_node)
  return (normal_nodes, reciprocal_nodes)


def contract_conditional_pattern_nodes(
    normal_nodes: List[Node], reciprocal_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  and_prob_list = []
  simple_prob_list = []
  for node in reciprocal_nodes[:]:     # P(A ^ B) / P(B) = P(A | B)
    exp_node = node.reciprocate()
    if exp_node.is_pure_node():
      simple_prob_list.append(exp_node.exp)
      reciprocal_nodes.remove(node)
  for node in normal_nodes[:]:
    if node.is_pure_node():
      and_prob = node.exp
      if type(and_prob) is AndProbabilityExpression and node in normal_nodes:
        and_prob_list.append(and_prob)
        normal_nodes.remove(node)
  (simple_prob_list,
   and_prob_list) = replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs(
       simple_prob_list, and_prob_list
       )
  normal_nodes += list(map(lambda x: Node(x), and_prob_list))
  reciprocal_nodes += list(map(lambda x: Node(x).reciprocate(), simple_prob_list))
  return (normal_nodes, reciprocal_nodes)


def replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs(
    simple_prob_list: List[BaseProbabilityExpression], and_prob_list: List[AndProbabilityExpression]
    ) -> Tuple[List[BaseProbabilityExpression], List[AndProbabilityExpression]]:
  for simple_prob in simple_prob_list[:]:
    for idx, and_exps in enumerate(and_prob_list[:]):
      if simple_prob == and_exps.base_exp:
        simple_prob_list.remove(simple_prob)
        and_prob_list[idx] = and_exps.aux_exp // simple_prob
        break
      elif simple_prob == and_exps.aux_exp:
        simple_prob_list.remove(simple_prob)
        and_prob_list[idx] = and_exps.base_exp // simple_prob
        break

  return (simple_prob_list, and_prob_list)


def contract_expanded_and_prob_exp(normal_node_list: List[Node]) -> List[Node]:
  (normal_nodes, conditional_exp_nodes) = split_normal_vs_conditional_exp_nodes(normal_node_list)
  if len(conditional_exp_nodes) == 0:
    return normal_node_list
  (normal_nodes, conditional_exp_nodes
   ) = replace_simple_vs_conditional_prob_lists_with_and_probs(normal_nodes, conditional_exp_nodes)
  return normal_nodes + conditional_exp_nodes


def split_normal_vs_conditional_exp_nodes(
    normal_node_list: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  conditional_exp_nodes = []
  normal_nodes = []
  for node in normal_node_list:
    if node.is_pure_node() and type(node.exp) is ConditionalProbabilityExpression:
      conditional_exp_nodes.append(node)
    else:
      normal_nodes.append(node)
  return (normal_nodes, conditional_exp_nodes)


def replace_simple_vs_conditional_prob_lists_with_and_probs(
    normal_nodes: List[Node], conditional_exp_nodes: List[Node]
    ) -> Tuple[List[Node], List[Node]]:
  for node in normal_nodes[:]:
    if node.is_pure_node():
      node_exp = node.exp
      for idx, conditional_node in enumerate(conditional_exp_nodes[:]):
        conditional_exp = conditional_node.exp
        if type(
            conditional_exp
            ) is ConditionalProbabilityExpression and conditional_exp.condition_exp == node_exp:     # P(A ^ B) = P(A | B) * P(B)
          conditional_exp_nodes[idx] = Node(
              conditional_exp.subject_exp & conditional_exp.condition_exp
              )
          normal_nodes.remove(node)
          break
  return (normal_nodes, conditional_exp_nodes)
