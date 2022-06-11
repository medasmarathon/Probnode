from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar
from probnode.interface.ioutcome import IOutcome


@dataclass(frozen=True, eq=True)
class Outcome(IOutcome):

  name: str = field()

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self.name})"


TDiscrete = TypeVar("TDiscrete")


@dataclass(frozen=True, eq=True)
class DiscreteOutcome(Outcome, Generic[TDiscrete]):

  discrete_value: TDiscrete = field(default=None, init=True)

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self.name}:{self.discrete_value})"