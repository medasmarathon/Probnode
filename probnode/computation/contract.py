from typing import Type, Union
from probnode.computation.node import *


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
  pass


def contract_arbitrary_product_node_group(node_list: List[Node]) -> List[Node]:
  pass