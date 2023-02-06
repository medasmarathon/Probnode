from dataclasses import dataclass, field
from typing import Any, Generic, List, Tuple, TypeVar
from probnode.interface.iexperiment import ITrialResult
from probnode.interface.ioutcome import IOutcome


@dataclass(frozen=True, eq=True)
class Outcome(IOutcome):

  name: str = field()
  trial_results: List[ITrialResult] = field(default=[])

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self.name})"


TDiscrete = TypeVar("TDiscrete")


@dataclass(frozen=True, eq=True)
class DiscreteOutcome(Outcome, Generic[TDiscrete]):

  discrete_value: TDiscrete = field(default=None, init=True)

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self.name}:{self.discrete_value})"


TRange = TypeVar("TRange")


@dataclass(frozen=True, eq=True)
class Range(Generic[TRange]):
  lower: TRange = field()
  upper: TRange = field()


@dataclass(frozen=True, eq=True)
class RangeOutcome(Outcome, Generic[TRange]):

  range_value: Range[TRange] = field(default=None, init=True)

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self.name}:[{self.range_value.lower},{self.range_value.upper}])"