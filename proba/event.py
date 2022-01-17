from proba.interface.iEvent import IEvent
from proba.probability import BaseProbability, POperator


class Event(IEvent):
  name: str

  def __init__(self, name: str):
    super().__init__()
    self.name = name

  def __repr__(self) -> str:
    return f"Event {self.__dict__}"
