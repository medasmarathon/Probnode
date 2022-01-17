from copy import deepcopy
from typing import List
from proba.interface.iEvent import IEvent
from proba.probability import BaseProbability, POperator


class DenomFreeProbabilityExpression(BaseProbability):

  @classmethod
  def from_event(cls, op: POperator, base_ev: IEvent):
    new_ins = DenomFreeProbabilityExpression(POperator.DEFAULT)
    new_ins.base_event = base_ev
    return new_ins

  base_node_tree: "DenomFreeProbabilityExpression"
  aux_node_tree: "DenomFreeProbabilityExpression"

  def __init__(
      self, op: POperator, base_tree: BaseProbability = None, aux_tree: BaseProbability = None
      ):
    super().__init__()
    self.operator = op
    self.base_node_tree = base_tree
    self.aux_node_tree = aux_tree

  def is_simple(self):
    if self.base_event is not None and self.base_node_tree is None:
      return True
    return False

  def __add__(self, other: BaseProbability):
    if self.operator == POperator.DEFAULT and other.operator == POperator.DEFAULT:
      return DenomFreeProbabilityExpression(POperator.OR, self, other)

  def __and__(self, other: BaseProbability):
    if self.operator == POperator.DEFAULT and other.operator == POperator.DEFAULT:
      return DenomFreeProbabilityExpression(POperator.AND, self, other)


class ProbabilityExpression(DenomFreeProbabilityExpression):
  numerator: "ProbabilityExpression" = None
  denominator: "ProbabilityExpression" = None

  def __floordiv__(self, other: "ProbabilityExpression"):
    condition_prob = ProbabilityExpression(POperator.CONDITION)
    condition_prob.numerator = self
    condition_prob.denominator = other
    return condition_prob
