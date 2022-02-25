from typing import Type, Union, TypeVar
from probnode.core.node import *
from probnode.computation.probability_expanding_logic import expand_probability_exp
from probnode.computation.util import _get_alternatives_from_list_of_possible_items


def expand(node: Node, exhausting: bool = False) -> List[Union[Node, ChainNode]]:
  if issubclass(type(node), ChainNode):
    return expand_chain_node(node, exhausting)
  if issubclass(type(node), DerivedNode):
    return expand_derived_node(node, exhausting)
  else:
    return expand_pure_node(node, exhausting)


def expand_pure_node(node: Node, exhausting: bool = False) -> List[Node]:
  if node.exp is None:     # node with fixed value
    return [node]
  return expand_probability_exp(node.exp)


def expand_derived_node(node: DerivedNode, exhausting: bool = False) -> List[Node]:
  if type(node) is AdditiveInverseNode:
    expanded_base = expand_pure_node(node.base, exhausting)
    return list(map(lambda x: AdditiveInverseNode.from_node(x), expanded_base))
  if type(node) is ReciprocalNode:
    expanded_base = expand_pure_node(node.base, exhausting)
    return list(map(lambda x: ReciprocalNode.from_node(x), expanded_base))
  return [node]


def expand_derived_chain_node(node: ChainNode, exhausting: bool = False) -> List[ChainNode]:
  if type(node) is AdditiveInverseChainNode:
    expanded_base = expand_chain_node(node.base, exhausting)
    return list(map(lambda x: AdditiveInverseChainNode.from_node(x), expanded_base))
  if type(node) is ReciprocalChainNode:
    expanded_base = expand_chain_node(node.base, exhausting)
    return list(map(lambda x: ReciprocalChainNode.from_node(x), expanded_base))
  return [node]


def expand_chain_node(chain_node: ChainNode, exhausting: bool = False) -> List[ChainNode]:
  aggregated_possible_chains = []
  for idx, node in enumerate(chain_node.args):
    if issubclass(type(node), ChainNode):
      if issubclass(type(node), DerivedNode):
        aggregated_possible_chains.append(expand_derived_chain_node(node))
      else:
        aggregated_possible_chains.append(expand_chain_node(node))
    elif issubclass(type(node), DerivedNode):
      aggregated_possible_chains.append(expand_derived_node(node))
    else:
      aggregated_possible_chains.append(expand_pure_node(node))
  possible_chains = _get_alternatives_from_list_of_possible_items(aggregated_possible_chains)
  result_chains = []
  for list_of_nodes in possible_chains:
    chain = _connect_nodes(type(chain_node), list_of_nodes)
    if chain is not None:
      result_chains.append(chain)
  return result_chains


def _connect_nodes(
    chain_type: Union[Type[SumNode], Type[ProductNode]], node_list: List[Node]
    ) -> Node:
  if chain_type is SumNode:
    chain_result = SumNode()
    chain_result.args = node_list
  if chain_type is ProductNode:
    chain_result = ProductNode()
    chain_result.args = node_list
  if chain_result is not None:
    return chain_result
