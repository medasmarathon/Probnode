from proba.computation.chain import AdditiveInverseNode, ChainNode, DerivedNode, Node, ReciprocalNode
from proba.computation.probabilityLogic import expand_probability_exp
from proba.probability import BaseProbabilityExpression


def expand(node: Node, exhausting: bool = False):
  if issubclass(type(node), ChainNode):
    return expand_chain_node(node, exhausting)
  if issubclass(type(node), DerivedNode):
    return expand_derived_node(node, exhausting)
  else:
    return expand_pure_node(node, exhausting)


def expand_pure_node(node: Node, exhausting: bool = False):
  return expand_probability_exp(node.exp)


def expand_derived_node(node: DerivedNode, exhausting: bool = False):
  if type(node) is AdditiveInverseNode:
    expanded_base = expand_pure_node(node.base, exhausting)
    return AdditiveInverseNode.from_node(expanded_base)
  if type(node) is ReciprocalNode:
    expanded_base = expand_pure_node(node.base, exhausting)
    return ReciprocalNode.from_node(expanded_base)
  return node


def expand_chain_node(chain_node: ChainNode, exhausting: bool = False):
  for idx, node in enumerate(chain_node.args):
    if issubclass(type(node), ChainNode):
      chain_node.args[idx] = expand_derived_node(node)
    elif issubclass(type(node), DerivedNode):
      chain_node.args[idx] = expand_derived_node(node)
    else:
      chain_node.args[idx] = expand_pure_node(node)
  return chain_node
