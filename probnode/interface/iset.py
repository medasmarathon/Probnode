from abc import ABC
from dataclasses import dataclass
from typing import Any, Set
from pyfields import field


@dataclass(unsafe_hash=True)
class BaseSet(ABC):
  set: Set[Any] = field(default=set())

  def __repr__(self) -> str:
    return self.set.__repr__()

  def __or__(self, other: "BaseSet"):
    or_set = OrSet()
    or_set.base = self
    or_set.aux = other
    return or_set

  def __and__(self, other: "BaseSet"):
    and_set = AndSet()
    and_set.base = self
    and_set.aux = other
    return and_set

  def __floordiv__(self, other: "BaseSet"):
    condition_set = ConditionalSet()
    condition_set.subject = self
    condition_set.condition = other
    return condition_set

  def invert(self) -> "BaseSet":
    raise NotImplementedError


class SimpleSet(BaseSet):

  def invert(self):
    not_set = SimpleInvertSet()
    not_set.set = self.set
    return not_set


class SimpleInvertSet(BaseSet):

  def invert(self):
    default_set = SimpleSet()
    default_set.set = self.set
    return default_set


class UnconditionalSet(BaseSet):
  base: "UnconditionalSet" = None
  aux: "UnconditionalSet" = None

  def invert(self):
    if type(self) is SimpleSet or type(self) is SimpleInvertSet:
      return super().invert()
    # TODO: Add inversion logic

  def __repr__(self) -> str:
    if self.set is not None:
      return f"{super().__repr__()}"
    if self.aux is None:
      return f"({self.base})"
    return f"({self.base} {self.aux})"


class AndSet(UnconditionalSet):

  def invert(self):
    invert_event = OrSet()
    invert_event.base = self.base.invert()
    invert_event.aux = self.aux.invert()
    return invert_event

  def __repr__(self) -> str:
    return f"{repr(self.base)} \u22C2 {repr(self.aux)}"


class OrSet(UnconditionalSet):

  def invert(self):
    invert_event = AndSet()
    invert_event.base = self.base.invert()
    invert_event.aux = self.aux.invert()
    return invert_event

  def __repr__(self) -> str:
    return f"{repr(self.base)} \u22C3 {repr(self.aux)}"


class ConditionalSet(UnconditionalSet):
  subject: "ConditionalSet" = None
  condition: "ConditionalSet" = None

  def __repr__(self) -> str:
    return f"{repr(self.subject)} \u2215 {repr(self.condition)}"
