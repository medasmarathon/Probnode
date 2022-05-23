from typing import Set
from pyfields import field
from dataclasses import dataclass
from probnode.interface.ioutcome import IOutcome


@dataclass(frozen=True, eq=True)
class SampleSpace:
  possible_outcomes: Set[IOutcome] = field(default=set())

  def __repr__(self) -> str:
    return f"\U0001D6C0={self.possible_outcomes}"
