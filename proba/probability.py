from copy import deepcopy
from enum import Enum
from proba.interface.iEvent import IEvent
from proba.interface.iProbability import IProbability
from proba.interface.iProbabilityExpression import IProbabilityExpression


class POperator(str, Enum):
  AND = "&&"
  OR = "V"
  NOT = "~"
  DEFAULT = ""
  CONDITION = "//"

  def __repr__(self) -> str:
    return self.value


class BaseProbabilityExpression(IProbability, IProbabilityExpression):
  operator: POperator = POperator.DEFAULT
  event: IEvent = None

  def invert(self):
    if self.operator == POperator.NOT:
      not_prob = deepcopy(self)
      not_prob.operator = POperator.DEFAULT
      return not_prob
    else:
      not_prob = deepcopy(self)
      not_prob.operator = POperator.NOT
      return not_prob

  def __repr__(self) -> str:
    return f"P({self.event.__repr__()})"


class SimpleProbabilityExpression(BaseProbabilityExpression):

  def invert(self):
    not_prob = SimpleInvertProbabilityExpression()
    not_prob.event = self.event
    return not_prob


class SimpleInvertProbabilityExpression(BaseProbabilityExpression):

  def invert(self):
    default_prob = SimpleProbabilityExpression()
    default_prob.event = self.event
    return default_prob

  def __repr__(self) -> str:
    return f"~P({self.event.__repr__()})"
