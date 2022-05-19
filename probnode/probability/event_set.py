from abc import ABC
from dataclasses import dataclass, field
from typing import overload
from probnode.interface.ioutcome import IOutcome
from probnode.interface.ievent import IEvent


@overload
def ES(expression: IOutcome) -> "SimpleEventSet":
  ...


@overload
def ES(expression: "BaseEventSet") -> "BaseEventSet":
  ...


def ES(expression):
  if isinstance(expression, IOutcome):
    return EventSet.from_outcome(expression)
  if isinstance(expression, BaseEventSet):
    return expression


@dataclass(unsafe_hash=True)
class BaseEventSet(IEvent, ABC):

  @classmethod
  def from_outcome(cls, base_outcome: IOutcome):
    new_ins = SimpleEventSet()
    new_ins.outcome = base_outcome
    return new_ins

  @classmethod
  def from_event(cls, event: "BaseEventSet"):
    return event

  outcome: IOutcome = field(init=False, default=None)

  def __repr__(self) -> str:
    return f"\U0001D6D4({self.outcome.__repr__()})"

  def __or__(self, other: "BaseEventSet"):
    or_event = OrEventSet()
    or_event.base_event = self
    or_event.aux_event = other
    return or_event

  def __and__(self, other: "BaseEventSet"):
    and_event = AndEventSet()
    and_event.base_event = self
    and_event.aux_event = other
    return and_event

  def __floordiv__(self, other: "BaseEventSet"):
    condition_event = ConditionalEventSet()
    condition_event.subject_event = self
    condition_event.condition_event = other
    return condition_event

  def invert(self) -> "BaseEventSet":
    raise NotImplementedError


class SimpleEventSet(BaseEventSet):
  """Event Set of only 1 **true** Outcome

  """

  def invert(self):
    not_event = SimpleInvertEventSet()
    not_event.outcome = self.outcome
    return not_event


class SimpleInvertEventSet(BaseEventSet):
  """Event Set of only 1 **false** Outcome

  """

  def invert(self):
    default_event = SimpleEventSet()
    default_event.outcome = self.outcome
    return default_event

  def __repr__(self) -> str:
    return f"\u00AC\U0001D6D4({self.outcome.__repr__()})"


class UnconditionalEventSet(BaseEventSet):
  base_event: "UnconditionalEventSet" = None
  aux_event: "UnconditionalEventSet" = None

  def invert(self):
    if type(self) is SimpleEventSet or type(self) is SimpleInvertEventSet:
      return super().invert()
    # TODO: Add inversion logic

  def __repr__(self) -> str:
    if self.outcome is not None:
      return f"{super().__repr__()}"
    if self.aux_event is None:
      return f"\U0001D6D4({self.base_event})"
    return f"\U0001D6D4({self.base_event} {self.aux_event})"


class AndEventSet(UnconditionalEventSet):

  def invert(self):
    invert_event = OrEventSet()
    invert_event.base_event = self.base_event.invert()
    invert_event.aux_event = self.aux_event.invert()
    return invert_event

  def __repr__(self) -> str:
    return f"\U0001D6D4({self.base_event} \u22C2 {self.aux_event})"


class OrEventSet(UnconditionalEventSet):

  def invert(self):
    invert_event = AndEventSet()
    invert_event.base_event = self.base_event.invert()
    invert_event.aux_event = self.aux_event.invert()
    return invert_event

  def __repr__(self) -> str:
    return f"\U0001D6D4({self.base_event} \u22C3 {self.aux_event})"


class ConditionalEventSet(UnconditionalEventSet):
  subject_event: "ConditionalEventSet" = None
  condition_event: "ConditionalEventSet" = None

  def __repr__(self) -> str:
    return f"\U0001D6D4({self.subject_event} \u2215 {self.condition_event})"


class EventSet(ConditionalEventSet):
  pass