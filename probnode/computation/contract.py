from typing import Tuple, Type, Union
from probnode import GenericSureEvent
from probnode.probability import *


def contract(chain: ChainP) -> ChainP:
  """Contract a `ChainP` (Chain Probability Measure) using fixed patterns (negating, complement, reciprocal,...)

  Args:
      chain (ChainP): Input ChainP

  Returns:
      ChainP: Contracted ChainP
  """
  if not issubclass(type(chain), ChainP):
    raise TypeError(f"Chain argument must be subclass of type {ChainP.__name__}")

  return contract_arbitrary_P_group(type(chain), chain.args)


def contract_arbitrary_P_group(
    chain_type: Union[Type[SumP], Type[ProductP]], P_list: List[ProbabilityMeasure]
    ) -> ChainP:
  if chain_type is SumP:
    result = SumP()
    result.args = contract_arbitrary_sum_P_group(P_list)

  if chain_type is ProductP:
    result = ProductP()
    result.args = contract_arbitrary_product_P_group(P_list)
  return result if result is not None else None


def contract_arbitrary_sum_P_group(
    P_list: List[Union[float, ProbabilityMeasure]]
    ) -> List[Union[float, ProbabilityMeasure]]:
  P_list = _convert_P_of_GenericSureEvent_in_P_list_to_float(P_list)
  (float_value, normal_additive_Ps,
   additive_inverse_Ps) = _split_float_vs_normal_vs_inverse_Ps(P_list)
  if _is_incontractible(normal_additive_Ps, additive_inverse_Ps):
    return [
        float_value
        ] + normal_additive_Ps + additive_inverse_Ps if float_value != 0 else normal_additive_Ps + additive_inverse_Ps

  (normal_additive_Ps, additive_inverse_Ps
   ) = remove_negating_Ps_from_classified_lists(normal_additive_Ps, additive_inverse_Ps)
  if _is_incontractible(normal_additive_Ps, additive_inverse_Ps):
    return [
        float_value
        ] + normal_additive_Ps + additive_inverse_Ps if float_value != 0 else normal_additive_Ps + additive_inverse_Ps

  (normal_additive_Ps, additive_inverse_Ps
   ) = remove_or_event_pattern_Ps_from_classified_lists(normal_additive_Ps, additive_inverse_Ps)
  if _is_incontractible(normal_additive_Ps, additive_inverse_Ps):
    return [float_value] + normal_additive_Ps if float_value != 0 else normal_additive_Ps

  (float_value, normal_additive_Ps,
   additive_inverse_Ps) = remove_complement_Ps_from_classified_lists(
       float_value, normal_additive_Ps, additive_inverse_Ps
       )

  if len(normal_additive_Ps) > 0:
    for idx, p in enumerate(normal_additive_Ps[:]):
      if issubclass(type(p), ChainP):
        normal_additive_Ps[idx] = contract(p)
  if len(additive_inverse_Ps) > 0:
    for idx, p in enumerate(additive_inverse_Ps[:]):
      invert_P = p.additive_invert()
      if issubclass(type(invert_P), ChainP):
        additive_inverse_Ps[idx] = contract(invert_P).additive_invert()
  return [
      float_value
      ] + normal_additive_Ps + additive_inverse_Ps if float_value != 0 else normal_additive_Ps + additive_inverse_Ps


def _is_incontractible(
    normal_additive_Ps: List[ProbabilityMeasure], additive_inverse_Ps: List[ProbabilityMeasure]
    ) -> bool:
  return len(additive_inverse_Ps) == 0 or len(normal_additive_Ps) == 0


def _convert_P_of_GenericSureEvent_in_P_list_to_float(
    P_list: List[Union[float, ProbabilityMeasure]]
    ) -> List[Union[float, ProbabilityMeasure]]:

  def is_P_of_GenericSureEvent(p: ProbabilityMeasure) -> bool:
    return p == ProbabilityMeasure(GenericSureEvent())

  def is_additive_inverse_P_of_GenericSureEvent(p: ProbabilityMeasure) -> bool:
    try:
      return p.additive_invert() == ProbabilityMeasure(GenericSureEvent())
    except AttributeError:
      return False

  def is_reciprocal_P_of_GenericSureEvent(p: ProbabilityMeasure) -> bool:
    try:
      return p.reciprocate() == ProbabilityMeasure(GenericSureEvent())
    except AttributeError:
      return False

  def try_convert_P_of_GenericSureEvent(p: ProbabilityMeasure) -> Union[ProbabilityMeasure, float]:
    if is_P_of_GenericSureEvent(p) or is_reciprocal_P_of_GenericSureEvent(p):
      return float(1)
    if is_additive_inverse_P_of_GenericSureEvent(p):
      return float(-1)
    return p

  return list(map(try_convert_P_of_GenericSureEvent, P_list))


def _split_float_vs_normal_vs_inverse_Ps(
    P_list: List[Union[float, ProbabilityMeasure]]
    ) -> Tuple[float, List[ProbabilityMeasure], List[ProbabilityMeasure]]:
  float_value = 0.0
  additive_inverse_Ps = []
  normal_additive_Ps = []
  for p in P_list:
    if isinstance(p, (int, float)):
      float_value = float_value + float(p)
    elif issubclass(type(p), AdditiveInverse):
      additive_inverse_Ps.append(p)
    else:
      normal_additive_Ps.append(p)
  return (float_value, normal_additive_Ps, additive_inverse_Ps)


def contract_negating_Ps(sum: SumP) -> SumP:
  """If `sum = ...+ P(A) + ... - P(A) +...` , then remove both `P(A)` and `- P(A)` in `sum`

  """
  P_list = _convert_P_of_GenericSureEvent_in_P_list_to_float(sum.args)
  (float_value, normal_additive_Ps,
   additive_inverse_Ps) = _split_float_vs_normal_vs_inverse_Ps(P_list)
  (normal_additive_Ps, additive_inverse_Ps
   ) = remove_negating_Ps_from_classified_lists(normal_additive_Ps, additive_inverse_Ps)
  contracted_sum = SumP()
  contracted_sum.args = [
      float_value
      ] + normal_additive_Ps + additive_inverse_Ps if float_value != 0 else normal_additive_Ps + additive_inverse_Ps
  return contracted_sum


def remove_negating_Ps_from_classified_lists(
    normal_additive_Ps: List[ProbabilityMeasure], additive_inverse_Ps: List[ProbabilityMeasure]
    ) -> Tuple[List[ProbabilityMeasure], List[ProbabilityMeasure]]:
  normal_Ps = normal_additive_Ps[:]
  invert_Ps = additive_inverse_Ps[:]
  for inverse_P in invert_Ps[:]:     # P(A) - P(A) = 0
    for normal_P in normal_Ps[:]:
      if inverse_P.additive_invert(
      ) == normal_P and normal_P in normal_Ps and inverse_P in invert_Ps:
        normal_Ps.remove(normal_P)
        invert_Ps.remove(inverse_P)
  return (normal_Ps, invert_Ps)


def contract_complement_Ps(sum: SumP) -> SumP:
  """If `sum = ...+ 1 + ... - P(not A) +...` , then replace both `1` and `- P(not A)` with `P(A)` in `sum`
  
    >>> contract_complement_nodes(1.5 - N(P(not A)))
        (0.5 + N(P(A)))
    >>> contract_complement_nodes(1 - N(P(not A)) + N(P(B)))
        (N(P(A)) + N(P(B)))

  """
  P_list = _convert_P_of_GenericSureEvent_in_P_list_to_float(sum.args)
  (float_value, normal_additive_Ps,
   additive_inverse_Ps) = _split_float_vs_normal_vs_inverse_Ps(P_list)
  (float_value, normal_additive_Ps,
   additive_inverse_Ps) = remove_complement_Ps_from_classified_lists(
       float_value, normal_additive_Ps, additive_inverse_Ps
       )
  contracted_sum = SumP()
  contracted_sum.args = [
      float_value
      ] + normal_additive_Ps + additive_inverse_Ps if float_value != 0 else normal_additive_Ps + additive_inverse_Ps
  return contracted_sum


def remove_complement_Ps_from_classified_lists(
    float_value: float, normal_additive_Ps: List[ProbabilityMeasure],
    additive_invert_Ps: List[ProbabilityMeasure]
    ) -> Tuple[float, List[ProbabilityMeasure], List[ProbabilityMeasure]]:
  """Replace complement nodes
        >>> remove_complement_nodes_from_classified_lists( 5,   # float value
                                                          [..., P(B),...], # Normal additive nodes
                                                          [... - P(not A),...]) # Invert additive nodes
            (4, [...,P(A), P(B),...], [...])
  """
  normal_Ps = normal_additive_Ps[:]
  invert_Ps = additive_invert_Ps[:]
  for p in invert_Ps[:]:
    if float_value >= 1:     # 1 - P(A) = P(not A)
      exp_P = p.additive_invert()
      if exp_P.is_pure_prob_measure():
        float_value = float_value - 1
        normal_Ps.append(ProbabilityMeasure(exp_P.event.complement()))
        invert_Ps.remove(p)
  return (float_value, normal_Ps, invert_Ps)


def contract_or_event_pattern_Ps(sum: SumP) -> SumP:
  """Contract all Or Probability patterns `P(A) + P(B) - P(A and B) = P(A or B)` in `sum`
  
    >>> contract_or_event_pattern_Ps(1.5 + N(P(A)) - N(P(A and B)) + N(P(B)))
        (0.5 + N(P(A or B)))

  """
  P_list = _convert_P_of_GenericSureEvent_in_P_list_to_float(sum.args)
  (float_value, normal_additive_Ps,
   additive_inverse_Ps) = _split_float_vs_normal_vs_inverse_Ps(P_list)
  (normal_additive_Ps, additive_inverse_Ps
   ) = remove_or_event_pattern_Ps_from_classified_lists(normal_additive_Ps, additive_inverse_Ps)
  contracted_sum = SumP()
  contracted_sum.args = [
      float_value
      ] + normal_additive_Ps + additive_inverse_Ps if float_value != 0 else normal_additive_Ps + additive_inverse_Ps
  return contracted_sum


def remove_or_event_pattern_Ps_from_classified_lists(
    normal_additive_Ps: List[ProbabilityMeasure], additive_invert_Ps: List[ProbabilityMeasure]
    ) -> Tuple[List[ProbabilityMeasure], List[ProbabilityMeasure]]:
  """Replace Or Event pattern Probability Measure with `OrProbabilityExpression`
        >>> remove_or_event_pattern_Ps_from_classified_lists([...P(A), P(B),...], # Normal additive probability measures
                                                                [... - P(A and B),...]) # Invert additive probability measures
            ([...P(A or B),...], [...])
  """
  normal_Ps = normal_additive_Ps[:]
  invert_Ps = additive_invert_Ps[:]
  andEvent_of_invert_P_list = []
  normal_event_list = []
  for p in normal_Ps[:]:
    if p.is_pure_prob_measure():
      normal_event_list.append(p.event)
      normal_Ps.remove(p)
  for p in invert_Ps[:]:
    inverted_P = p.additive_invert()
    if inverted_P.is_pure_prob_measure():
      and_event = inverted_P.event
      if type(and_event) is AndEvent and p in invert_Ps:
        andEvent_of_invert_P_list.append(and_event)
        invert_Ps.remove(p)
  (normal_event_list, andEvent_of_invert_P_list
   ) = replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
       normal_event_list, andEvent_of_invert_P_list
       )
  normal_Ps += list(map(lambda x: ProbabilityMeasure(x), normal_event_list))
  invert_Ps += list(
      map(lambda x: ProbabilityMeasure(x).additive_invert(), andEvent_of_invert_P_list)
      )
  return (normal_Ps, invert_Ps)


def replace_or_pattern_members_in_normalEvent_list_vs_andEvent_of_invert_P_list_with_P_of_OrEvent(
    normal_event_list: List[BaseEvent], and_event_list: List[AndEvent]
    ) -> Tuple[List[BaseEvent], List[AndEvent]]:
  """Replace Probability measure in Or Event pattern with corresponding probability measure of `OrEvent`
        >>> replace_pattern_member_in_atomic_vs_and_event_lists_with_P_of_OrEvent([...P(A), P(B),...], [...P(A and B),...])
          ([...P(A or B),...], [...])
  """
  children_of_and_event_list = list(map(lambda x: [x.base_event, x.aux_event], and_event_list))
  for normal_event in normal_event_list[:]:
    for idx, children_events in enumerate(children_of_and_event_list[:]):
      if normal_event in children_events:
        children_events.remove(normal_event)
        if len(children_events) == 0:
          normal_event_list.remove(and_event_list[idx].aux_event)
          normal_event_list.remove(and_event_list[idx].base_event)
          normal_event_list.append(and_event_list[idx].base_event | and_event_list[idx].aux_event)
          and_event_list.pop(idx)
        break

  return (normal_event_list, and_event_list)


def contract_arbitrary_product_P_group(
    P_list: List[Union[float, ProbabilityMeasure]]
    ) -> List[Union[float, ProbabilityMeasure]]:
  P_list = _convert_P_of_GenericSureEvent_in_P_list_to_float(P_list)
  (float_value, normal_Ps, reciprocal_Ps) = _split_float_vs_normal_vs_reciprocal_Ps(P_list)
  if len(reciprocal_Ps) == 0 or len(normal_Ps) == 0:
    return [float_value] + simplify_expanded_P_of_AndEvent(
        normal_Ps + reciprocal_Ps
        ) if float_value != 1 else simplify_expanded_P_of_AndEvent(normal_Ps + reciprocal_Ps)

  (normal_Ps, reciprocal_Ps) = remove_reciprocal_Ps_from_classified_lists(normal_Ps, reciprocal_Ps)
  if len(reciprocal_Ps) == 0 or len(normal_Ps) == 0:
    return [float_value] + reciprocal_Ps + simplify_expanded_P_of_AndEvent(
        normal_Ps
        ) if float_value != 1 else reciprocal_Ps + simplify_expanded_P_of_AndEvent(normal_Ps)

  (normal_Ps,
   reciprocal_Ps) = simplify_Ps_of_ConditionalEvent_from_classified_lists(normal_Ps, reciprocal_Ps)

  normal_Ps = simplify_expanded_P_of_AndEvent(normal_Ps)

  if len(normal_Ps) > 0:
    for idx, p in enumerate(normal_Ps[:]):
      if issubclass(type(p), ChainP):
        normal_Ps[idx] = contract(p)
  if len(reciprocal_Ps) > 0:
    for idx, p in enumerate(reciprocal_Ps[:]):
      invert_P = p.additive_invert()
      if issubclass(type(invert_P), ChainP):
        reciprocal_Ps[idx] = contract(invert_P).additive_invert()
  return [
      float_value
      ] + normal_Ps + reciprocal_Ps if float_value != 1 else normal_Ps + reciprocal_Ps


def _split_float_vs_normal_vs_reciprocal_Ps(
    P_list: List[Union[float, ProbabilityMeasure]]
    ) -> Tuple[float, List[ProbabilityMeasure], List[ProbabilityMeasure]]:
  float_value = 1.0
  reciprocal_Ps = []
  normal_Ps = []
  for p in P_list:
    if isinstance(p, (int, float)):
      float_value = float_value * float(p)
    elif issubclass(type(p), Reciprocal):
      reciprocal_Ps.append(p)
    else:
      normal_Ps.append(p)
  return (float_value, normal_Ps, reciprocal_Ps)


def contract_reciprocated_Ps(product: ProductP) -> ProductP:
  """Contract reciprocated probability measures `P(A) / P(A) = 1` in `product`
  
    >>> contract_reciprocated_Ps(1.5 * N(P(A)) / N(P(A)) * N(P(B)))
        (1.5 * N(P(B)))

  """
  P_list = _convert_P_of_GenericSureEvent_in_P_list_to_float(product.args)
  (float_value, normal_product_Ps, reciprocal_Ps) = _split_float_vs_normal_vs_reciprocal_Ps(P_list)
  (normal_product_Ps,
   reciprocal_Ps) = remove_reciprocal_Ps_from_classified_lists(normal_product_Ps, reciprocal_Ps)
  contracted_product = SumP()
  contracted_product.args = [
      float_value
      ] + normal_product_Ps + reciprocal_Ps if float_value != 1 else normal_product_Ps + reciprocal_Ps
  return contracted_product


def remove_reciprocal_Ps_from_classified_lists(
    normal_Ps: List[ProbabilityMeasure], reciprocal_Ps: List[ProbabilityMeasure]
    ) -> Tuple[List[ProbabilityMeasure], List[ProbabilityMeasure]]:
  for reciproc_P in reciprocal_Ps[:]:     #  P(A) / P(A) = 1
    for normal_P in normal_Ps[:]:
      if reciproc_P.reciprocate(
      ) == normal_P and normal_P in normal_Ps and reciproc_P in reciprocal_Ps:
        normal_Ps.remove(normal_P)
        reciprocal_Ps.remove(reciproc_P)
  return (normal_Ps, reciprocal_Ps)


def contract_Ps_of_ConditionalEvent(product: ProductP) -> ProductP:
  """Contract probability measures of ConditionalEvent ` P(X and Y) / P(Y) = P(X when Y)` in `product`
  
    >>> contract_Ps_of_ConditionalEvent(1.5 * N(P(A and B)) / N(P(A)) * N(P(B)))
        (1.5 * N(P(B when A)) * N(P(B)))

  """
  P_list = _convert_P_of_GenericSureEvent_in_P_list_to_float(product.args)
  (float_value, normal_product_Ps, reciprocal_Ps) = _split_float_vs_normal_vs_reciprocal_Ps(P_list)
  (normal_product_Ps, reciprocal_Ps
   ) = simplify_Ps_of_ConditionalEvent_from_classified_lists(normal_product_Ps, reciprocal_Ps)
  contracted_product = SumP()
  contracted_product.args = [
      float_value
      ] + normal_product_Ps + reciprocal_Ps if float_value != 1 else normal_product_Ps + reciprocal_Ps
  return contracted_product


def simplify_Ps_of_ConditionalEvent_from_classified_lists(
    normal_Ps: List[ProbabilityMeasure], reciprocal_Ps: List[ProbabilityMeasure]
    ) -> Tuple[List[ProbabilityMeasure], List[ProbabilityMeasure]]:     # P(A ^ B) / P(B) = P(A | B)

  (reciprocals_prob_list,
   and_prob_list) = _filter_Event_of_reciprocals_and_AndEvents_from_Ps(reciprocal_Ps, normal_Ps)
  (reciprocals_prob_list,
   and_prob_list) = replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent(
       reciprocals_prob_list, and_prob_list
       )
  normal_Ps += list(map(lambda x: ProbabilityMeasure(x), and_prob_list))
  reciprocal_Ps += list(map(lambda x: ProbabilityMeasure(x).reciprocate(), reciprocals_prob_list))
  return (normal_Ps, reciprocal_Ps)


def _filter_Event_of_reciprocals_and_AndEvents_from_Ps(
    reciprocal_Ps: List[ReciprocalP], normal_Ps: List[ProbabilityMeasure]
    ) -> Tuple[List[BaseEvent], List[AndEvent]]:

  and_event_list = []
  reciprocals_event_list = []
  for p in reciprocal_Ps[:]:
    rec_p = p.reciprocate()
    if rec_p.is_pure_prob_measure():
      reciprocals_event_list.append(rec_p.event)
      reciprocal_Ps.remove(p)
  for p in normal_Ps[:]:
    if p.is_pure_prob_measure():
      and_event = p.event
      if type(and_event) is AndEvent and p in normal_Ps:
        and_event_list.append(and_event)
        normal_Ps.remove(p)

  return (reciprocals_event_list, and_event_list)


def replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent(
    reciprocals_event_list: List[BaseEvent], and_event_list: List[AndEvent]
    ) -> Tuple[List[BaseEvent], List[AndEvent]]:
  """Replace events in conditional event pattern `P(A and B) / P(A) = P(B when A)` with corresponding ConditionalEvent
        >>> replace_reciprocal_Events_vs_AndEvent_lists_with_ConditionalEvent([... A (of P(A)),...], [...(A and B) (of P(A and B)),...])
          ([...,...], [..., (B when A) (of P(B when A)) ],...)
  """
  for reciprocal_event in reciprocals_event_list[:]:
    for idx, and_event in enumerate(and_event_list[:]):
      if reciprocal_event == and_event.base_event:     # check if X of P(X) is either A or B of P(A and B)
        reciprocals_event_list.remove(reciprocal_event)
        and_event_list[
            idx
            ] = and_event.aux_event // reciprocal_event     # replace P(A and B) and P(X) with either P(X when A) or P(X when B)
        break
      elif reciprocal_event == and_event.aux_event:
        reciprocals_event_list.remove(reciprocal_event)
        and_event_list[idx] = and_event.base_event // reciprocal_event
        break

  return (reciprocals_event_list, and_event_list)


def contract_expanded_Ps_of_AndEvent(
    product: ProductP
    ) -> ProductP:     # P(A and B) = P(A when B) * P(B)
  """Contract expanded Probability Measure of AndEvent ` P(Y) * P(X when Y) = P(X and Y)` in `product`
  
    >>> contract_expanded_Ps_of_AndEvent(1.5 * N(P(A when B)) * N(P(B)))
        (1.5 * N(P(B and A)))

  """
  P_list = _convert_P_of_GenericSureEvent_in_P_list_to_float(product.args)
  (float_value, normal_product_Ps, reciprocal_Ps) = _split_float_vs_normal_vs_reciprocal_Ps(P_list)
  normal_product_Ps = simplify_expanded_P_of_AndEvent(normal_product_Ps)
  contracted_product = SumP()
  contracted_product.args = [
      float_value
      ] + normal_product_Ps + reciprocal_Ps if float_value != 1 else normal_product_Ps + reciprocal_Ps
  return contracted_product


def simplify_expanded_P_of_AndEvent(
    normal_P_list: List[ProbabilityMeasure]
    ) -> List[ProbabilityMeasure]:
  (normal_Ps, conditional_event_Ps) = split_normal_vs_ConditionalEvent_Ps(normal_P_list)
  if len(conditional_event_Ps) == 0:
    return normal_P_list
  (normal_Ps, conditional_event_Ps
   ) = _replace_product_P_lists_with_equivalent_AndEvent_Ps(normal_Ps, conditional_event_Ps)
  return normal_Ps + conditional_event_Ps


def split_normal_vs_ConditionalEvent_Ps(
    normal_P_list: List[ProbabilityMeasure]
    ) -> Tuple[List[ProbabilityMeasure], List[ProbabilityMeasure]]:
  conditional_event_Ps = []
  normal_Ps = []
  for p in normal_P_list:
    if p.is_pure_prob_measure() and type(p.event) is ConditionalEvent:
      conditional_event_Ps.append(p)
    else:
      normal_Ps.append(p)
  return (normal_Ps, conditional_event_Ps)


def _replace_product_P_lists_with_equivalent_AndEvent_Ps(
    normal_Ps: List[ProbabilityMeasure], conditional_event_Ps: List[ProbabilityMeasure]
    ) -> Tuple[List[ProbabilityMeasure], List[ProbabilityMeasure]]:
  for p in normal_Ps[:]:
    if p.is_pure_prob_measure():
      node_exp = p.event
      for idx, conditional_event_P in enumerate(conditional_event_Ps[:]):
        conditional_event = conditional_event_P.event
        if type(
            conditional_event
            ) is ConditionalEvent and conditional_event.condition_event == node_exp:     # P(A and B) = P(A when B) * P(B)
          conditional_event_Ps[idx] = ProbabilityMeasure(
              conditional_event.subject_event & conditional_event.condition_event
              )
          normal_Ps.remove(p)
          break
  return (normal_Ps, conditional_event_Ps)
