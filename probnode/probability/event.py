from dataclasses import dataclass, field
from probnode.interface.ievent import IEvent


@dataclass(frozen=True, eq=True)
class Event(IEvent):

  name: str = field()

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}{self.__dict__}"


class SureEvent(IEvent):

  def __repr__(self) -> str:
    return f"SureEvent{self.__dict__}"
