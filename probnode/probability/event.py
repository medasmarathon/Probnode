from dataclasses import dataclass
from probnode.interface.ievent import IEvent


@dataclass
class Event(IEvent):
  name: str

  def __init__(self, name: str):
    super().__init__()
    self.name = name

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}{self.__dict__}"


class SureEvent(IEvent):

  def __repr__(self) -> str:
    return f"SureEvent{self.__dict__}"
