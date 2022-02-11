from typing import Union
from probnode.computation.node import *
from probnode.computation.probabilityExpandingLogic import expand_probability_exp


def expand(node: Node, exhausting: bool = False) -> List[Union[Node, ChainNode]]:
  if issubclass(type(node), ChainNode):
    return expand_chain_node(node, exhausting)
  if issubclass(type(node), DerivedNode):
    return expand_derived_node(node, exhausting)
  else:
    return expand_pure_node(node, exhausting)


def expand_pure_node(node: Node, exhausting: bool = False) -> List[Node]:
  return expand_probability_exp(node.exp)


def expand_derived_node(node: DerivedNode, exhausting: bool = False) -> List[Node]:
  if type(node) is AdditiveInverseNode:
    expanded_base = expand_pure_node(node.base, exhausting)
    return [AdditiveInverseNode.from_node(expanded_base)]
  if type(node) is ReciprocalNode:
    expanded_base = expand_pure_node(node.base, exhausting)
    return [ReciprocalNode.from_node(expanded_base)]
  return [node]


def expand_derived_chain_node(node: ChainNode, exhausting: bool = False) -> List[ChainNode]:
  if type(node) is AdditiveInverseChainNode:
    expanded_base = expand_chain_node(node.base, exhausting)
    return [AdditiveInverseChainNode.from_node(expanded_base)]
  if type(node) is ReciprocalChainNode:
    expanded_base = expand_chain_node(node.base, exhausting)
    return [ReciprocalChainNode.from_node(expanded_base)]
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
  possible_chains = get_alternatives_from_list_of_possible_items(aggregated_possible_chains)
  return possible_chains


def get_alternatives_from_list_of_possible_items(possible_list: List[List[object]]):
  if len(possible_list) > 1:
    last_items = possible_list.pop()
    last_alternatives = get_alternatives_from_list_of_possible_items(possible_list)
    possible_chains = []
    for alternative in last_alternatives:
      for item in last_items:
        possible_chains.append(alternative + [item])
    return possible_chains
  elif len(possible_list) == 1:
    return list(map(lambda x: [x], possible_list[0]))
