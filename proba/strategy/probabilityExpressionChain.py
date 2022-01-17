from typing import List

from proba.interface.iProbabilityExpression import IProbabilityExpression, ProbExpressionMathNotation
from proba.probability import BaseProbabilityExpression


class ProbabilityExpressionChain:
  chain: List[IProbabilityExpression] = []

  def with_prob_exp(self, prob_exp: BaseProbabilityExpression):
    self.chain.append(prob_exp)
    return self

  def do(self, math_notation: ProbExpressionMathNotation):
    self.chain.append(math_notation)
    return self

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}::{self.chain}"