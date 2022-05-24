from typing import List, Set
from dataclasses import dataclass, field
from probnode.interface.ioutcome import IOutcome


@dataclass(unsafe_hash=True, eq=True)
class SampleSpace:
  __possible_outcomes: Set[IOutcome] = field()

  def __init__(self, possible_outcomes: List[IOutcome] = []):
    self.__possible_outcomes = set(possible_outcomes)

  def __repr__(self) -> str:
    return f"\U0001D6C0={self.__possible_outcomes}"

  def has_outcome(self, outcome: IOutcome) -> bool:
    if outcome in self.__possible_outcomes:
      return True
    return False

  def get_outcome_set(self) -> Set[IOutcome]:
    return self.__possible_outcomes