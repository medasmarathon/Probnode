from enum import Enum
from proba.interface.iEvent import IEvent
from proba.interface.iProbability import IProbability


class POperator(Enum):
  AND = "&"
  OR = "+"
  NOT = "~"
  DEFAULT = "d"


class BaseProbability(IProbability):
  operator: POperator = POperator.DEFAULT
  base_event: IEvent = None
  aux_event: IEvent = None
