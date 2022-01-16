from proba.interface.iProbabilityExpression import IProbabilityExpression


class ProbabilityExpression(IProbabilityExpression):
  numerator: IProbabilityExpression
  denominator: IProbabilityExpression
