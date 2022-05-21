from typing import List, Type, Union
from probnode.probability.probability_measure import *
from probnode.probability.event_set import GenericSureEventSet
from probnode.probability.event_set import *
from probnode import ES__


def contract_pattern_node_group(
    chain_type: Union[Type[SumP], Type[ProductP]], node_list: List[ProbabilityMeasure]
    ) -> List[ProbabilityMeasure]:
  if len(node_list) == 2:
    result = contract_2_nodes(chain_type, node_list)
  elif len(node_list) == 3 and chain_type is SumP:
    result = contract_sum_3_nodes(node_list)

  if result is not None:
    return result
  return node_list


def contract_2_nodes(
    chain_type: Union[Type[SumP], Type[ProductP]], node_list: List[ProbabilityMeasure]
    ) -> Union[ProbabilityMeasure, None]:
  if chain_type is SumP:
    return try_contract_sum_2_nodes(node_list)
  if chain_type is ProductP:
    return contract_product_2_nodes(node_list)


def try_contract_sum_2_nodes(
    sum_nodes: List[ProbabilityMeasure]
    ) -> Union[ProbabilityMeasure, None]:
  if len(sum_nodes) != 2:
    raise ValueError("List parameter must have 2 nodes")
  node1 = sum_nodes[0]
  node2 = sum_nodes[1]
  if is_complement_pattern(node1, node2):
    return ProbabilityMeasure(node2.event_set.invert())
  if is_negating_pattern(node1, node2):
    return ProbabilityMeasure(None, 0)
  return None


def contract_sum_3_nodes(sum_nodes: List[ProbabilityMeasure]) -> Union[ProbabilityMeasure, None]:
  if len(sum_nodes) != 3:
    raise ValueError("List parameter must have 3 nodes")
  result = try_contract_or_probability_pattern(sum_nodes[0], sum_nodes[1], sum_nodes[2])
  if result is not None:
    return result


def contract_product_2_nodes(
    product_nodes: List[ProbabilityMeasure]
    ) -> Union[ProbabilityMeasure, None]:
  if len(product_nodes) != 2:
    raise ValueError("List parameter must have 2 nodes")
  node1 = product_nodes[0]
  node2 = product_nodes[1]
  if is_reciprocal_pattern(node1, node2):     # P(A) / P(A) = 1
    return ProbabilityMeasure(None, 1)

  conditional_probnode = try_contract_conditional_probability_pattern(
      node1, node2
      )     # P(A ^ B) / P(B) = P(A | B)
  if conditional_probnode is not None:
    return conditional_probnode

  if node1.event_set is not None and node2.event_set is not None:     # default is joint probability: P(A)P(B) = P(A ^ B)
    return ProbabilityMeasure(ES__(node1.event_set & node2.event_set))
  return None


def is_complement_pattern(sure_event: ProbabilityMeasure, event_node: ProbabilityMeasure) -> bool:
  if type(sure_event.event_set
          ) is GenericSureEventSet and issubclass(type(event_node),
                                                  AdditiveInverse):     # 1 - P(A) = P(not A)
    return True
  return False


def is_negating_pattern(
    event_node: ProbabilityMeasure, inverse_event_node: ProbabilityMeasure
    ) -> bool:
  if event_node in [AdditiveInverseP.from_P(inverse_event_node),
                    AdditiveInverseChainP.from_P(inverse_event_node)]:     # P(A) vs - P(A)
    return True
  return False


def is_reciprocal_pattern(
    event_node: ProbabilityMeasure, reciprocal_event_node: ProbabilityMeasure
    ) -> bool:
  if event_node in [ReciprocalP.from_P(reciprocal_event_node),
                    ReciprocalChainP.from_P(reciprocal_event_node)]:     # P(A) vs 1/ P(A)
    return True
  return False


def is_conditional_probability_pattern(
    node_A_and_B: ProbabilityMeasure, reciprocal_node_B: ProbabilityMeasure
    ) -> bool:     # P(A ^ B) / P(B)
  if node_A_and_B.event_set is None or (not issubclass(type(reciprocal_node_B), Reciprocal)):
    return False
  A_and_B_exp = node_A_and_B.event_set
  B_exp = reciprocal_node_B.reciprocate().event_set
  if type(A_and_B_exp) is AndEventSet and B_exp in [A_and_B_exp.base_event, A_and_B_exp.aux_event]:
    return True
  return False


def try_contract_conditional_probability_pattern(
    node_A_and_B: ProbabilityMeasure, reciprocal_node_B: ProbabilityMeasure
    ) -> Union[ProbabilityMeasure, None]:     # P(A ^ B) / P(B)
  if node_A_and_B.event_set is None or (not issubclass(type(reciprocal_node_B), Reciprocal)):
    return None
  A_and_B_exp = node_A_and_B.event_set
  B_exp = reciprocal_node_B.reciprocate().event_set
  if type(A_and_B_exp) is AndEventSet and (B_exp in [A_and_B_exp.base_event, A_and_B_exp.aux_event
                                                     ]):
    numerator_exps = [A_and_B_exp.base_event, A_and_B_exp.aux_event]
    A_exp = list(filter(lambda x: x != B_exp, numerator_exps)).pop()
    return ProbabilityMeasure(ES__(A_exp // B_exp))
  return None


def is_or_probability_pattern(
    node1: ProbabilityMeasure, node2: ProbabilityMeasure, node3: ProbabilityMeasure
    ) -> bool:     # P(A) + P(B) - P(A ^ B) = P(A v B)
  for node in [node1, node2, node3]:
    additive_invert_node = node.additive_invert()
    if type(additive_invert_node.event_set) is AndEventSet:
      other_nodes = list(filter(lambda x: x != node, [node1, node2, node3]))
      other_exps = map(lambda x: x.event_set if x.event_set is not None else None, other_nodes)
      if set(other_exps) == set([additive_invert_node.event_set.aux_event,
                                 additive_invert_node.event_set.base_event]):
        return True
  return False


def try_contract_or_probability_pattern(
    node1: ProbabilityMeasure, node2: ProbabilityMeasure, node3: ProbabilityMeasure
    ) -> Union[ProbabilityMeasure, None]:
  for node in [node1, node2, node3]:
    additive_invert_node = node.additive_invert()
    if type(additive_invert_node.event_set) is AndEventSet:
      other_nodes = list(filter(lambda x: x != node, [node1, node2, node3]))
      other_exps = map(lambda x: x.event_set if x.event_set is not None else None, other_nodes)
      if set(other_exps) == set([additive_invert_node.event_set.aux_event,
                                 additive_invert_node.event_set.base_event]):
        return ProbabilityMeasure(
            additive_invert_node.event_set.base_event | additive_invert_node.event_set.aux_event
            )
  return None