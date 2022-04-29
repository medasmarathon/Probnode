from probnode.datatype.probability_value import ProbabilityValue
from pyfields import field


class IProbability:
  value: ProbabilityValue = field(default=None)
