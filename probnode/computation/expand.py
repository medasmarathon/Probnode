from typing import Type, Union, TypeVar
from probnode.probability.probability_measure import *
from probnode.computation.probability_expanding_logic import expand_probability_exp
from probnode.computation.util import _get_alternatives_from_list_of_possible_items


def expand(node: ProbabilityMeasure,
           exhausting: bool = False) -> List[Union[ProbabilityMeasure, ChainP]]:
  if issubclass(type(node), ChainP):
    return expand_chain_node(node, exhausting)
  if issubclass(type(node), DerivedP):
    return expand_derived_node(node, exhausting)
  else:
    return expand_pure_node(node, exhausting)


def expand_pure_node(node: ProbabilityMeasure,
                     exhausting: bool = False) -> List[ProbabilityMeasure]:
  if node.event_set is None:     # node with fixed value
    return [node]
  return expand_probability_exp(node.event_set)


def expand_derived_node(node: DerivedP, exhausting: bool = False) -> List[ProbabilityMeasure]:
  if type(node) is AdditiveInverseP:
    expanded_base = expand_pure_node(node.base, exhausting)
    return list(map(lambda x: AdditiveInverseP.from_P(x), expanded_base))
  if type(node) is ReciprocalP:
    expanded_base = expand_pure_node(node.base, exhausting)
    return list(map(lambda x: ReciprocalP.from_P(x), expanded_base))
  return [node]


def expand_derived_chain_node(node: ChainP, exhausting: bool = False) -> List[ChainP]:
  if type(node) is AdditiveInverseChainP:
    expanded_base = expand_chain_node(node.base, exhausting)
    return list(map(lambda x: AdditiveInverseChainP.from_P(x), expanded_base))
  if type(node) is ReciprocalChainP:
    expanded_base = expand_chain_node(node.base, exhausting)
    return list(map(lambda x: ReciprocalChainP.from_P(x), expanded_base))
  return [node]


def expand_chain_node(chain_node: ChainP, exhausting: bool = False) -> List[ChainP]:
  aggregated_possible_chains = []
  for idx, node in enumerate(chain_node.args):
    if issubclass(type(node), ChainP):
      if issubclass(type(node), DerivedP):
        aggregated_possible_chains.append(expand_derived_chain_node(node))
      else:
        aggregated_possible_chains.append(expand_chain_node(node))
    elif issubclass(type(node), DerivedP):
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
    chain_type: Union[Type[SumP], Type[ProductP]], node_list: List[ProbabilityMeasure]
    ) -> ProbabilityMeasure:
  if chain_type is SumP:
    chain_result = SumP()
    chain_result.args = node_list
  if chain_type is ProductP:
    chain_result = ProductP()
    chain_result.args = node_list
  if chain_result is not None:
    return chain_result
