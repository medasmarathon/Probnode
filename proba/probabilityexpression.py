from typing import List
from proba.interface.iEvent import IEvent
from proba.probability import BaseProbabilityExpression, POperator


class UnconditionalProbabilityExpression(BaseProbabilityExpression):

  @classmethod
  def from_event(cls, op: POperator, base_ev: IEvent):
    new_ins = UnconditionalProbabilityExpression(POperator.DEFAULT)
    new_ins.event = base_ev
    return new_ins

  @classmethod
  def from_expression(cls, expression: BaseProbabilityExpression):
    return expression

  base_exp: "UnconditionalProbabilityExpression" = None
  aux_exp: "UnconditionalProbabilityExpression" = None

  def __init__(self, op: POperator = None):
    super().__init__()
    if op is not None:
      self.operator = op

  def is_simple(self):
    if self.event is not None and self.base_exp is None:
      return True
    return False

  def __add__(self, other: BaseProbabilityExpression):
    if self.operator == POperator.DEFAULT and other.operator == POperator.DEFAULT:
      or_prob = UnconditionalProbabilityExpression(POperator.OR)
      or_prob.base_exp = self
      or_prob.aux_exp = other
      return or_prob

  def __and__(self, other: BaseProbabilityExpression):
    if self.operator == POperator.DEFAULT and other.operator == POperator.DEFAULT:
      and_prob = UnconditionalProbabilityExpression(POperator.AND)
      and_prob.base_exp = self
      and_prob.aux_exp = other
      return and_prob

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