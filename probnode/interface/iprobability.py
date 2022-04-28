from probnode.datatype.probabilityvalue import ProbabilityValue
from pyfields import field


class IProbability:
  value: ProbabilityValue = field(default=None)
