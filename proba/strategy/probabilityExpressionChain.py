from typing import List

from proba.interface.iProbabilityExpression import IProbabilityExpression, PMathNotation
from proba.probability import BaseProbabilityExpression


class ProbabilityExpressionChain:
  chain: List[IProbabilityExpression] = []

  def __repr__(self) -> str:
    return " ".join(repr(item) for item in self.chain)