from dataclasses import dataclass, field
from probnode.interface.ioutcome import IOutcome


@dataclass(frozen=True, eq=True)
class Outcome(IOutcome):

  name: str = field()

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self.name})"
