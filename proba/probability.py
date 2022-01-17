from copy import deepcopy
from enum import Enum
from proba.interface.iEvent import IEvent
from proba.interface.iProbability import IProbability


class POperator(str, Enum):
  AND = "&"
  OR = "+"
  NOT = "~"
  DEFAULT = "d"
  CONDITION = "//"

  def __repr__(self) -> str:
    return self.value


class BaseProbability(IProbability):
  operator: POperator = POperator.DEFAULT
  base_event: IEvent = None

  def invert(self):
    if self.operator == POperator.DEFAULT:
      not_prob = deepcopy(self)
      not_prob.operator = POperator.NOT
      return not_prob
    if self.operator == POperator.NOT:
      not_prob = deepcopy(self)
      not_prob.operator = POperator.DEFAULT
      return not_prob

  def __repr__(self) -> str:
    return f"{self.__class__} {self.__dict__}"
