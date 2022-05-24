from typing import List, Type, Union
from probnode.probability.probability_measure import *
from probnode.probability.event import GenericSureEvent
from probnode.probability.event import *
from probnode import Event


def contract_pattern_P_group(
    chain_type: Union[Type[SumP], Type[ProductP]], p_list: List[ProbabilityMeasure]
    ) -> List[ProbabilityMeasure]:
  if len(p_list) == 2:
    result = contract_2_Ps(chain_type, p_list)
  elif len(p_list) == 3 and chain_type is SumP:
    result = contract_sum_3_Ps(p_list)

  if result is not None:
    return result
  return p_list


def contract_2_Ps(chain_type: Union[Type[SumP], Type[ProductP]],
                  p_list: List[ProbabilityMeasure]) -> Union[ProbabilityMeasure, None]:
  if chain_type is SumP:
    return try_contract_sum_2_Ps(p_list)
  if chain_type is ProductP:
    return contract_product_2_Ps(p_list)


def try_contract_sum_2_Ps(sum_Ps: List[ProbabilityMeasure]) -> Union[ProbabilityMeasure, None]:
  if len(sum_Ps) != 2:
    raise ValueError("List parameter must have 2 nodes")
  p1 = sum_Ps[0]
  p2 = sum_Ps[1]
  if is_complement_pattern(p1, p2):
    return ProbabilityMeasure(p2.event.complement())
  if is_negating_pattern(p1, p2):
    return ProbabilityMeasure(None, 0)
  return None


def contract_sum_3_Ps(sum_Ps: List[ProbabilityMeasure]) -> Union[ProbabilityMeasure, None]:
  if len(sum_Ps) != 3:
    raise ValueError("List parameter must have 3 nodes")
  result = try_contract_OrEvent_pattern(sum_Ps[0], sum_Ps[1], sum_Ps[2])
  if result is not None:
    return result


def contract_product_2_Ps(product_Ps: List[ProbabilityMeasure]) -> Union[ProbabilityMeasure, None]:
  if len(product_Ps) != 2:
    raise ValueError("List parameter must have 2 nodes")
  p1 = product_Ps[0]
  p2 = product_Ps[1]
  if is_reciprocal_pattern(p1, p2):     # P(A) / P(A) = 1
    return ProbabilityMeasure(None, 1)

  p_of_ConditionalEvent = try_contract_ConditionalEvent_pattern(
      p1, p2
      )     # P(A ^ B) / P(B) = P(A | B)
  if p_of_ConditionalEvent is not None:
    return p_of_ConditionalEvent

  if p1.event is not None and p2.event is not None:     # default is joint probability: P(A)P(B) = P(A ^ B)
    return ProbabilityMeasure(Event(p1.event & p2.event))
  return None


def is_complement_pattern(
    p_of_SureEvent: ProbabilityMeasure, p_of_event: ProbabilityMeasure
    ) -> bool:
  if type(p_of_SureEvent.event
          ) is GenericSureEvent and issubclass(type(p_of_event),
                                               AdditiveInverse):     # 1 - P(A) = P(not A)
    return True
  return False


def is_negating_pattern(p: ProbabilityMeasure, inverse_p: ProbabilityMeasure) -> bool:
  if p in [AdditiveInverseP.from_P(inverse_p),
           AdditiveInverseChainP.from_P(inverse_p)]:     # P(A) vs - P(A)
    return True
  return False


def is_reciprocal_pattern(p: ProbabilityMeasure, reciprocal_p: ProbabilityMeasure) -> bool:
  if p in [ReciprocalP.from_P(reciprocal_p),
           ReciprocalChainP.from_P(reciprocal_p)]:     # P(A) vs 1/ P(A)
    return True
  return False


def is_conditional_probability_pattern(
    p_of_A_and_B: ProbabilityMeasure, reciprocal_p_of_B: ProbabilityMeasure
    ) -> bool:     # P(A ^ B) / P(B)
  if p_of_A_and_B.event is None or (not issubclass(type(reciprocal_p_of_B), Reciprocal)):
    return False
  A_and_B_event = p_of_A_and_B.event
  B_event = reciprocal_p_of_B.reciprocate().event
  if type(A_and_B_event) is AndEvent and B_event in [A_and_B_event.base_event,
                                                     A_and_B_event.aux_event]:
    return True
  return False


def try_contract_ConditionalEvent_pattern(
    p_of_A_and_B: ProbabilityMeasure, reciprocal_p_of_B: ProbabilityMeasure
    ) -> Union[ProbabilityMeasure, None]:     # P(A ^ B) / P(B)
  if p_of_A_and_B.event is None or (not issubclass(type(reciprocal_p_of_B), Reciprocal)):
    return None
  A_and_B_event = p_of_A_and_B.event
  B_event = reciprocal_p_of_B.reciprocate().event
  if type(A_and_B_event) is AndEvent and (B_event in [A_and_B_event.base_event,
                                                      A_and_B_event.aux_event]):
    numerator_events = [A_and_B_event.base_event, A_and_B_event.aux_event]
    A_event = list(filter(lambda x: x != B_event, numerator_events)).pop()
    return ProbabilityMeasure(Event(A_event // B_event))
  return None


def is_OrEvent_pattern(
    p1: ProbabilityMeasure, p2: ProbabilityMeasure, p3: ProbabilityMeasure
    ) -> bool:     # P(A) + P(B) - P(A ^ B) = P(A v B)
  for p in [p1, p2, p3]:
    additive_invert_p = p.additive_invert()
    if type(additive_invert_p.event) is AndEvent:
      other_Ps = list(filter(lambda x: x != p, [p1, p2, p3]))
      other_events = map(lambda x: x.event if x.event is not None else None, other_Ps)
      if set(other_events) == set([additive_invert_p.event.aux_event,
                                   additive_invert_p.event.base_event]):
        return True
  return False


def try_contract_OrEvent_pattern(
    p1: ProbabilityMeasure, p2: ProbabilityMeasure, p3: ProbabilityMeasure
    ) -> Union[ProbabilityMeasure, None]:
  for p in [p1, p2, p3]:
    additive_invert_p = p.additive_invert()
    if type(additive_invert_p.event) is AndEvent:
      other_Ps = list(filter(lambda x: x != p, [p1, p2, p3]))
      other_events = map(lambda x: x.event if x.event is not None else None, other_Ps)
      if set(other_events) == set([additive_invert_p.event.aux_event,
                                   additive_invert_p.event.base_event]):
        return ProbabilityMeasure(
            additive_invert_p.event.base_event | additive_invert_p.event.aux_event
            )
  return None