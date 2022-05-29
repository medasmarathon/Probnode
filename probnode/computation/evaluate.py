from typing import Optional
from probnode.probability.event import GenericSureEvent
from probnode.probability import *


def eval(p_of_event: ProbabilityMeasureOfEvent) -> Optional[float]:
  if type(p_of_event) is DerivedP:
    return evaluate_derived_p(p_of_event)
  elif type(p_of_event) is ChainP:
    return evaluate_chain_p(p_of_event)
  return evaluate_simple(p_of_event)


def evaluate_simple(p_of_event: ProbabilityMeasureOfEvent) -> Optional[float]:
  if p_of_event.event is None:
    return None
  if type(p_of_event.event) == GenericSureEvent:
    return float(1)
  return p_of_event.random_var(p_of_event.event)


def evaluate_derived_p(p_of_event: DerivedP) -> Optional[float]:
  if type(p_of_event) is AdditiveInverseP:
    return evaluate_additive_invert_p(p_of_event)
  if type(p_of_event) is ReciprocalP:
    return evaluate_reciprocal_p(p_of_event)


def evaluate_additive_invert_p(p_of_event: AdditiveInverseP) -> Optional[float]:
  if eval(p_of_event.base) is not None:
    return 0 - eval(p_of_event.base)
  return None


def evaluate_reciprocal_p(p_of_event: ReciprocalP) -> Optional[float]:
  if eval(p_of_event.base) is not None and eval(p_of_event.base) != 0:
    return 1 / eval(p_of_event.base)
  return None


def evaluate_chain_p(p_of_event: ChainP) -> Optional[float]:
  if type(p_of_event) is SumP:
    return evaluate_sum_p(p_of_event)
  if type(p_of_event) is ProductP:
    return evaluate_product_p(p_of_event)


def evaluate_sum_p(p_of_event: SumP) -> Optional[float]:
  if None in list(map(lambda x: _get_value_of_chain_item(x), p_of_event.args)):
    return None
  return sum(list(map(lambda x: eval(x), p_of_event.args)))


def evaluate_product_p(p_of_event: ProductP) -> Optional[float]:
  if len(p_of_event.args) == 0:
    return 1.0
  if None in list(map(lambda x: _get_value_of_chain_item(x), p_of_event.args)):
    return None
  return math.prod(list(map(lambda x: eval(x), p_of_event.args)))


def _get_value_of_chain_item(self, item: Union[float,
                                               ProbabilityMeasureOfEvent]) -> Optional[float]:
  if isinstance(item, (int, float)):
    return item
  else:
    return eval(item)
