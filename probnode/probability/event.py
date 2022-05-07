from abc import ABC
from dataclasses import dataclass, field
from typing import overload
from probnode.interface.ioutcome import IOutcome
from probnode.interface.ievent import IEvent


@overload
def E(expression: IOutcome) -> "SimpleEvent":
  ...


@overload
def E(expression: "BaseEvent") -> "BaseEvent":
  ...


def E(expression):
  if isinstance(expression, IOutcome):
    return Event.from_outcome(expression)
  if isinstance(expression, BaseEvent):
    return expression


@dataclass(unsafe_hash=True)
class BaseEvent(IEvent, ABC):

  @classmethod
  def from_outcome(cls, base_outcome: IOutcome):
    new_ins = SimpleEvent()
    new_ins.outcome = base_outcome
    return new_ins

  @classmethod
  def from_event(cls, event: "BaseEvent"):
    return event

  outcome: IOutcome = field(init=False, default=None)

  def __repr__(self) -> str:
    return f"\u2119({self.outcome.__repr__()})"

  def __or__(self, other: "BaseEvent"):
    or_prob = OrEvent()
    or_prob.base_event = self
    or_prob.aux_event = other
    return or_prob

  def __and__(self, other: "BaseEvent"):
    and_prob = AndEvent()
    and_prob.base_event = self
    and_prob.aux_event = other
    return and_prob

  def __floordiv__(self, other: "BaseEvent"):
    condition_prob = ConditionalEvent()
    condition_prob.subject_event = self
    condition_prob.condition_event = other
    return condition_prob

  def invert(self) -> "BaseEvent":
    raise NotImplementedError


class SimpleEvent(BaseEvent):

  def invert(self):
    not_prob = SimpleInvertEvent()
    not_prob.outcome = self.outcome
    return not_prob


class SimpleInvertEvent(BaseEvent):

  def invert(self):
    default_prob = SimpleEvent()
    default_prob.outcome = self.outcome
    return default_prob

  def __repr__(self) -> str:
    return f"\u00AC\u2119({self.outcome.__repr__()})"


class UnconditionalEvent(BaseEvent):
  base_event: "UnconditionalEvent" = None
  aux_event: "UnconditionalEvent" = None

  def invert(self):
    if type(self) is SimpleEvent or type(self) is SimpleInvertEvent:
      return super().invert()
    # TODO: Add inversion logic

  def __repr__(self) -> str:
    if self.outcome is not None:
      return f"{super().__repr__()}"
    if self.aux_event is None:
      return f"\u2119({self.base_event})"
    return f"\u2119({self.base_event} {self.aux_event})"


class AndEvent(UnconditionalEvent):

  def invert(self):
    invert_prob = OrEvent()
    invert_prob.base_event = self.base_event.invert()
    invert_prob.aux_event = self.aux_event.invert()
    return invert_prob

  def __repr__(self) -> str:
    return f"\u2119({self.base_event} \u22C2 {self.aux_event})"


class OrEvent(UnconditionalEvent):

  def invert(self):
    invert_prob = AndEvent()
    invert_prob.base_event = self.base_event.invert()
    invert_prob.aux_event = self.aux_event.invert()
    return invert_prob

  def __repr__(self) -> str:
    return f"\u2119({self.base_event} \u22C3 {self.aux_event})"


class ConditionalEvent(UnconditionalEvent):
  subject_event: "ConditionalEvent" = None
  condition_event: "ConditionalEvent" = None

  def __repr__(self) -> str:
    return f"\u2119({self.subject_event} \u2215 {self.condition_event})"


class Event(ConditionalEvent):
  pass