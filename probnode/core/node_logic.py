from probnode.core.node import N, AdditiveInverse, AdditiveInverseChainNode, AdditiveInverseNode, ChainNode, Node, ReciprocalChainNode, ReciprocalNode


def is_pure_node(node: Node) -> bool:
  if type(node) in [Node, N]:
    return True
  return False


def reciprocate(node: Node) -> Node:
  if issubclass(type(node), ChainNode):
    return ReciprocalChainNode.from_node(node)
  return ReciprocalNode.from_node(node)


def additive_invert(node: Node) -> Node:
  if issubclass(type(node), ChainNode):
    return AdditiveInverseChainNode.from_node(node)
  return AdditiveInverseNode.from_node(node)