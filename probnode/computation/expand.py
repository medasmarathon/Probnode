from typing import Type, Union, TypeVar
from probnode.probability.probability_measure import *
from probnode.computation.probability_expanding_logic import expand_and_apply_P_on_event
from probnode.computation.util import _get_alternatives_from_list_of_possible_items


def expand(p: ProbabilityMeasure,
           exhausting: bool = False) -> List[Union[ProbabilityMeasure, ChainP]]:
  if issubclass(type(p), ChainP):
    return expand_chain_P(p, exhausting)
  if issubclass(type(p), DerivedP):
    return expand_derived_P(p, exhausting)
  else:
    return expand_pure_P(p, exhausting)


def expand_pure_P(p: ProbabilityMeasure, exhausting: bool = False) -> List[ProbabilityMeasure]:
  if p.event is None:     # node with fixed value
    return [p]
  return expand_and_apply_P_on_event(p.event)


def expand_derived_P(derived_p: DerivedP, exhausting: bool = False) -> List[ProbabilityMeasure]:
  if type(derived_p) is AdditiveInverseP:
    expanded_base = expand_pure_P(derived_p.base, exhausting)
    return list(map(lambda x: AdditiveInverseP.from_P(x), expanded_base))
  if type(derived_p) is ReciprocalP:
    expanded_base = expand_pure_P(derived_p.base, exhausting)
    return list(map(lambda x: ReciprocalP.from_P(x), expanded_base))
  return [derived_p]


def expand_derived_chain_P(chain_p: ChainP, exhausting: bool = False) -> List[ChainP]:
  if type(chain_p) is AdditiveInverseChainP:
    expanded_base = expand_chain_P(chain_p.base, exhausting)
    return list(map(lambda x: AdditiveInverseChainP.from_P(x), expanded_base))
  if type(chain_p) is ReciprocalChainP:
    expanded_base = expand_chain_P(chain_p.base, exhausting)
    return list(map(lambda x: ReciprocalChainP.from_P(x), expanded_base))
  return [chain_p]


def expand_chain_P(chain_node: ChainP, exhausting: bool = False) -> List[ChainP]:
  aggregated_possible_chains = []
  for idx, p in enumerate(chain_node.args):
    if issubclass(type(p), ChainP):
      if issubclass(type(p), DerivedP):
        aggregated_possible_chains.append(expand_derived_chain_P(p))
      else:
        aggregated_possible_chains.append(expand_chain_P(p))
    elif issubclass(type(p), DerivedP):
      aggregated_possible_chains.append(expand_derived_P(p))
    else:
      aggregated_possible_chains.append(expand_pure_P(p))
  possible_chains = _get_alternatives_from_list_of_possible_items(aggregated_possible_chains)
  result_chains = []
  for list_of_nodes in possible_chains:
    chain = _connect_Ps(type(chain_node), list_of_nodes)
    if chain is not None:
      result_chains.append(chain)
  return result_chains


def _connect_Ps(
    chain_type: Union[Type[SumP], Type[ProductP]], p_list: List[ProbabilityMeasure]
    ) -> ProbabilityMeasure:
  if chain_type is SumP:
    chain_result = SumP()
    chain_result.args = p_list
  if chain_type is ProductP:
    chain_result = ProductP()
    chain_result.args = p_list
  if chain_result is not None:
    return chain_result
