from typing import List
from proba.probability import BaseProbability, POperator


class DenomFreeProbabilityExpression(BaseProbability):

  @classmethod
  def invert(cls, prob: BaseProbability):
    if prob.operator == POperator.DEFAULT:
      return DenomFreeProbabilityExpression(POperator.NOT, prob)

  expression_nodes: List["DenomFreeProbabilityExpression"]

  def __add__(self, other: BaseProbability):
    if self.operator == POperator.DEFAULT and other.operator == POperator.DEFAULT:
      return DenomFreeProbabilityExpression(POperator.OR, self, other)

  def __and__(self, other: BaseProbability):
    if self.operator == POperator.DEFAULT and other.operator == POperator.DEFAULT:
      return DenomFreeProbabilityExpression(POperator.AND, self, other)


class ProbabilityExpression(DenomFreeProbabilityExpression):
  numerator: DenomFreeProbabilityExpression
  denominator: DenomFreeProbabilityExpression
