from typing import Type, Union
from probnode import P
from probnode.computation.node import *
from probnode.computation.nodeLogic import additive_invert, is_pure_node


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
  additive_inverse_nodes = []
  normal_additive_nodes = []
  for node in node_list:
    if issubclass(type(node), AdditiveInverse):
      additive_inverse_nodes.append(node)
    else:
      normal_additive_nodes.append(node)
  if len(additive_inverse_nodes) == 0:
    return node_list

  for invert_node in additive_inverse_nodes[:]:
    for node in normal_additive_nodes[:]:
      if additive_invert(invert_node) == node:
        normal_additive_nodes.remove(node)
        additive_inverse_nodes.remove(invert_node)
  if len(additive_inverse_nodes) == 0 or len(normal_additive_nodes) == 0:
    return additive_inverse_nodes + normal_additive_nodes

  for node in normal_additive_nodes[:]:
    if node == Node(P(SureEvent())) and len(additive_inverse_nodes) > 0:
      exp_node = additive_invert(additive_inverse_nodes[0])
      if is_pure_node(exp_node):
        normal_additive_nodes.append(Node(exp_node.exp.invert()))
        additive_inverse_nodes.pop(0)
  if len(additive_inverse_nodes) == 0:
    return normal_additive_nodes


def contract_arbitrary_product_node_group(node_list: List[Node]) -> List[Node]:
  pass