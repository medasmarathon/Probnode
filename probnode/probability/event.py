from abc import ABC
from dataclasses import dataclass, field
from typing import Union, overload, Set
from probnode.interface.ioutcome import IOutcome
from probnode.interface.ievent import IEvent


@overload
def Event(outcome: IOutcome) -> "AtomicEvent":
  ...


@overload
def Event(event: "BaseEvent") -> "BaseEvent":
  ...


def Event(
    expression: Union[IOutcome, "BaseEvent"]
    ) -> Union["AtomicEvent", "ComplementaryAtomicEvent", "UnconditionalEvent", "ConditionalEvent"]:
  """In probability theory, an event is a set of outcomes of an experiment (a subset of the sample space) to which a probability is assigned.

  https://en.wikipedia.org/wiki/Event_(probability_theory)
  """
  if isinstance(expression, IOutcome):
    return GenericEvent.from_outcome(expression)
  if isinstance(expression, BaseEvent):
    return expression


@dataclass(unsafe_hash=True)
class BaseEvent(IEvent, ABC):

  outcome: IOutcome = field(init=False, default=None)

  def __repr__(self) -> str:
    return f"\U0001D6D4{{{self.outcome.__repr__()}}}"

  def __or__(self, other: "BaseEvent"):
    or_event = OrEvent()
    or_event.base_event = self
    or_event.aux_event = other
    return or_event

  def __and__(self, other: "BaseEvent"):
    and_event = AndEvent()
    and_event.base_event = self
    and_event.aux_event = other
    return and_event

  def __floordiv__(self, other: "BaseEvent"):
    condition_event = ConditionalEvent()
    condition_event.subject_event = self
    condition_event.condition_event = other
    return condition_event

  def complement(self) -> "BaseEvent":
    raise NotImplementedError

  def get_outcome_set(self) -> Set[IOutcome]:
    return set([self.outcome])


class AtomicEvent(BaseEvent):
  """An event consisting of only a single outcome is called an elementary event or an atomic event; that is, it is a singleton set

  https://en.wikipedia.org/wiki/Event_(probability_theory)

  """

  def complement(self):
    not_event = ComplementaryAtomicEvent()
    not_event.outcome = self.outcome
    return not_event


class ComplementaryAtomicEvent(BaseEvent):
  """ The complement of any event A is the event [not A], i.e. the event that A does not occur. Here A is atomic event

  https://en.wikipedia.org/wiki/Complementary_event

  """

  def complement(self):
    default_event = AtomicEvent()
    default_event.outcome = self.outcome
    return default_event

  def __repr__(self) -> str:
    return f"\u00AC\U0001D6D4{{{self.outcome.__repr__()}}}"


class UnconditionalEvent(BaseEvent):
  base_event: "UnconditionalEvent" = None
  aux_event: "UnconditionalEvent" = None

  def complement(self):
    if type(self) is AtomicEvent or type(self) is ComplementaryAtomicEvent:
      return super().complement()
    raise NotImplementedError

  def get_outcome_set(self) -> Set[IOutcome]:
    return self.base_event.get_outcome_set().union(self.aux_event.get_outcome_set())

  def __repr__(self) -> str:
    if self.outcome is not None:
      return f"{super().__repr__()}"
    if self.aux_event is None:
      return f"\U0001D6D4{{{self.base_event}}}"
    return f"\U0001D6D4{{{self.base_event} {self.aux_event}}}"


class AndEvent(UnconditionalEvent):

  def complement(self):
    invert_event = OrEvent()
    invert_event.base_event = self.base_event.complement()
    invert_event.aux_event = self.aux_event.complement()
    return invert_event

  def __repr__(self) -> str:
    return f"\U0001D6D4{{{self.base_event} \u22C2 {self.aux_event}}}"


class OrEvent(UnconditionalEvent):

  def complement(self):
    invert_event = AndEvent()
    invert_event.base_event = self.base_event.complement()
    invert_event.aux_event = self.aux_event.complement()
    return invert_event

  def __repr__(self) -> str:
    return f"\U0001D6D4{{{self.base_event} \u22C3 {self.aux_event}}}"


class ConditionalEvent(UnconditionalEvent):
  subject_event: "ConditionalEvent" = None
  condition_event: "ConditionalEvent" = None

  def get_outcome_set(self) -> Set[IOutcome]:
    return self.subject_event.get_outcome_set().union(self.condition_event.get_outcome_set())

  def __repr__(self) -> str:
    return f"\U0001D6D4{{{self.subject_event} \u2215 {self.condition_event}}}"


class GenericEvent(ConditionalEvent):

  @classmethod
  def from_outcome(cls, base_outcome: IOutcome):
    evt = AtomicEvent()
    evt.outcome = base_outcome
    return evt


class GenericSureEvent(BaseEvent):

  def __repr__(self) -> str:
    return f"\U0001D6D4{{ \U0001D6C0 }}"
