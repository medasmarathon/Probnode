from copy import deepcopy
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

  def invert(self):
    if self.is_simple():
      return super().invert()
    if self.operator == POperator.AND:
      invert_prob = UnconditionalProbabilityExpression(POperator.OR)
      invert_prob.base_exp = self.base_exp.invert()
      invert_prob.aux_exp = self.aux_exp.invert() if self.aux_exp is not None else None
      return invert_prob
    if self.operator == POperator.OR:
      invert_prob = UnconditionalProbabilityExpression(POperator.AND)
      invert_prob.base_exp = self.base_exp.invert()
      invert_prob.aux_exp = self.aux_exp.invert() if self.aux_exp is not None else None
      return invert_prob

  def __or__(self, other: BaseProbabilityExpression):
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

  def __repr__(self) -> str:
    if self.event is not None:
      return f"{self.operator}{super().__repr__()}"
    if self.aux_exp is None:
      return f"P({self.operator}{self.base_exp})"
    return f"P({self.base_exp} {self.operator} {self.aux_exp})"


class ConditionalProbabilityExpression(UnconditionalProbabilityExpression):
  subject_exp: "ConditionalProbabilityExpression" = None
  condition_exp: "ConditionalProbabilityExpression" = None


class ProbabilityExpression(ConditionalProbabilityExpression):
  pass