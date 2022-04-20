from abc import ABC
from dataclasses import dataclass
from probnode.interface.ievent import IEvent
from probnode.interface.iprobability import IProbability
from probnode.interface.iprobability_expression import IProbabilityExpression


def P(expression):
  if isinstance(expression, IEvent):
    return ProbabilityExpression.from_event(expression)
  if isinstance(expression, BaseProbabilityExpression):
    return expression


@dataclass
class BaseProbabilityExpression(IProbability, IProbabilityExpression, ABC):

  @classmethod
  def from_event(cls, base_ev: IEvent):
    new_ins = SimpleProbabilityExpression()
    new_ins.event = base_ev
    return new_ins

  @classmethod
  def from_expression(cls, expression: "BaseProbabilityExpression"):
    return expression

  event: IEvent = None

  def __repr__(self) -> str:
    return f"\u2119({self.event.__repr__()})"

  def __hash__(self) -> int:
    return hash(self.__repr__())

  def __or__(self, other: "BaseProbabilityExpression"):
    or_prob = OrProbabilityExpression()
    or_prob.base_exp = self
    or_prob.aux_exp = other
    return or_prob

  def __and__(self, other: "BaseProbabilityExpression"):
    and_prob = AndProbabilityExpression()
    and_prob.base_exp = self
    and_prob.aux_exp = other
    return and_prob

  def __floordiv__(self, other: "BaseProbabilityExpression"):
    condition_prob = ConditionalProbabilityExpression()
    condition_prob.subject_exp = self
    condition_prob.condition_exp = other
    return condition_prob

  def invert(self) -> "BaseProbabilityExpression":
    raise NotImplementedError


class SimpleProbabilityExpression(BaseProbabilityExpression):

  def invert(self):
    not_prob = SimpleInvertProbabilityExpression()
    not_prob.event = self.event
    return not_prob


class SimpleInvertProbabilityExpression(BaseProbabilityExpression):

  def invert(self):
    default_prob = SimpleProbabilityExpression()
    default_prob.event = self.event
    return default_prob

  def __repr__(self) -> str:
    return f"\u00AC\u2119({self.event.__repr__()})"


class UnconditionalProbabilityExpression(BaseProbabilityExpression):
  base_exp: "UnconditionalProbabilityExpression" = None
  aux_exp: "UnconditionalProbabilityExpression" = None

  def invert(self):
    if type(self) is SimpleProbabilityExpression or type(self) is SimpleInvertProbabilityExpression:
      return super().invert()
    # TODO: Add inversion logic

  def __repr__(self) -> str:
    if self.event is not None:
      return f"{super().__repr__()}"
    if self.aux_exp is None:
      return f"\u2119({self.base_exp})"
    return f"\u2119({self.base_exp} {self.aux_exp})"


class AndProbabilityExpression(UnconditionalProbabilityExpression):

  def invert(self):
    invert_prob = OrProbabilityExpression()
    invert_prob.base_exp = self.base_exp.invert()
    invert_prob.aux_exp = self.aux_exp.invert()
    return invert_prob

  def __repr__(self) -> str:
    return f"\u2119({self.base_exp} \u22C2 {self.aux_exp})"


class OrProbabilityExpression(UnconditionalProbabilityExpression):

  def invert(self):
    invert_prob = AndProbabilityExpression()
    invert_prob.base_exp = self.base_exp.invert()
    invert_prob.aux_exp = self.aux_exp.invert()
    return invert_prob

  def __repr__(self) -> str:
    return f"\u2119({self.base_exp} \u22C3 {self.aux_exp})"


class ConditionalProbabilityExpression(UnconditionalProbabilityExpression):
  subject_exp: "ConditionalProbabilityExpression" = None
  condition_exp: "ConditionalProbabilityExpression" = None

  def __repr__(self) -> str:
    return f"\u2119({self.subject_exp} \u2215 {self.condition_exp})"


class ProbabilityExpression(ConditionalProbabilityExpression):
  pass