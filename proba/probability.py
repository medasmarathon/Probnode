from enum import Enum
from proba.interface.iEvent import IEvent
from proba.interface.iProbability import IProbability


class POperator(Enum):
  AND = "&"
  OR = "+"
  NOT = "~"
  DEFAULT = "d"


class BaseProbability(IProbability):
  operator: POperator
  base_event: IEvent
  aux_event: IEvent

  def __init__(self, op: POperator, base_ev: IEvent, aux_event: IEvent = None):
    super().__init__()
    self.operator = POperator.DEFAULT
    self.base_event = base_ev
    self.aux_event = aux_event
