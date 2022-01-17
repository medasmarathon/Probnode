from copy import deepcopy
from typing import List
from proba.interface.iEvent import IEvent
from proba.probability import BaseProbability, POperator


class UnconditionalProbabilityExpression(BaseProbability):

  @classmethod
  def from_event(cls, op: POperator, base_ev: IEvent):
    new_ins = UnconditionalProbabilityExpression(POperator.DEFAULT)
    new_ins.base_event = base_ev
    return new_ins

  base_exp: "UnconditionalProbabilityExpression"
  aux_exp: "UnconditionalProbabilityExpression"

  def __init__(
      self, op: POperator, base_tree: BaseProbability = None, aux_tree: BaseProbability = None
      ):
    super().__init__()
    self.operator = op
    self.base_exp = base_tree
    self.aux_exp = aux_tree

  def is_simple(self):
    if self.base_event is not None and self.base_exp is None:
      return True
    return False

  def __add__(self, other: BaseProbability):
    if self.operator == POperator.DEFAULT and other.operator == POperator.DEFAULT:
      return UnconditionalProbabilityExpression(POperator.OR, self, other)

  def __and__(self, other: BaseProbability):
    if self.operator == POperator.DEFAULT and other.operator == POperator.DEFAULT:
      return UnconditionalProbabilityExpression(POperator.AND, self, other)

  def __floordiv__(self, other: "UnconditionalProbabilityExpression"):
    condition_prob = ConditionalProbabilityExpression(POperator.CONDITION)
    condition_prob.subject_exp = self
    condition_prob.condition_exp = other
    return condition_prob


class ConditionalProbabilityExpression(UnconditionalProbabilityExpression):
  subject_exp: "ConditionalProbabilityExpression" = None
  condition_exp: "ConditionalProbabilityExpression" = None


class ProbabilityExpression(ConditionalProbabilityExpression):
  pass