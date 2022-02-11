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
    return AdditiveInverseNode.from_node(expanded_base)
  if type(node) is ReciprocalNode:
    expanded_base = expand_pure_node(node.base, exhausting)
    return ReciprocalNode.from_node(expanded_base)
  return node


def expand_derived_chain_node(node: ChainNode, exhausting: bool = False) -> List[ChainNode]:
  if type(node) is AdditiveInverseChainNode:
    expanded_base = expand_chain_node(node.base, exhausting)
    return AdditiveInverseChainNode.from_node(expanded_base)
  if type(node) is ReciprocalChainNode:
    expanded_base = expand_chain_node(node.base, exhausting)
    return ReciprocalChainNode.from_node(expanded_base)
  return node


def expand_chain_node(chain_node: ChainNode, exhausting: bool = False) -> List[ChainNode]:
  for idx, node in enumerate(chain_node.args):
    if issubclass(type(node), ChainNode):
      if issubclass(type(node), DerivedNode):
        chain_node.args[idx] = expand_derived_chain_node(node)
      else:
        chain_node.args[idx] = expand_chain_node(node)
    elif issubclass(type(node), DerivedNode):
      chain_node.args[idx] = expand_derived_node(node)
    else:
      chain_node.args[idx] = expand_pure_node(node)
  return chain_node
