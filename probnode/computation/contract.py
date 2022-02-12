from probnode.computation.node import *


def contract(chain: ChainNode) -> Node:
  if not issubclass(type(chain), ChainNode):
    raise TypeError(f"Chain argument must be subclass of type {ChainNode.__name__}")

  if len(chain.args) == 1:
    return chain
  elif len(chain.a) == 2:
    return contract_2_nodes(chain)
  elif len(chain.args) == 3:
    return contract_3_nodes(chain)
  else:
    pass


def contract_2_nodes(chain: ChainNode):
  pass


def contract_3_nodes(chain: ChainNode):
  pass