from probnode.computation.node import AdditiveInverse, AdditiveInverseChainNode, ChainNode, Node, ReciprocalChainNode, ReciprocalNode


def is_pure_node(node: Node) -> bool:
  return False


def reciprocate(node: Node) -> Node:
  if issubclass(type(node), ChainNode):
    return ReciprocalChainNode.from_node(node)
  return ReciprocalNode.from_node(node)


def additive_invert(node: Node) -> Node:
  if issubclass(type(node), ChainNode):
    return AdditiveInverseChainNode.from_node(node)
  return AdditiveInverse.from_node(node)