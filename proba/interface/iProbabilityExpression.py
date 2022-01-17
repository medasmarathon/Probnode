from enum import Enum


class IProbabilityExpression:
  pass


class PMathNotation(IProbabilityExpression, Enum):
  ADD = "+"
  SUBTRACT = "-"
  MULTIPLY = "*"
  DIVIDE = "/"

  def __repr__(self) -> str:
    return self.value
