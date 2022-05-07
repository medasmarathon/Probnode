from abc import ABC
from dataclasses import dataclass, field
from typing import overload
from probnode.interface.ioutcome import IOutcome
from probnode.interface.iprobability import IProbability
from probnode.interface.iprobability_expression import IProbabilityExpression


@overload
def P(expression: IOutcome) -> "SimpleProbabilityExpression":
  ...


@overload
def P(expression: "BaseProbabilityExpression") -> "BaseProbabilityExpression":
  ...


def P(expression):
  if isinstance(expression, IOutcome):
    return ProbabilityExpression.from_event(expression)
  if isinstance(expression, BaseProbabilityExpression):
    return expression


@dataclass(unsafe_hash=True)
class BaseProbabilityExpression(IProbability, IProbabilityExpression, ABC):

  @classmethod
  def from_event(cls, base_ev: IOutcome):
    new_ins = SimpleProbabilityExpression()
    new_ins.outcome = base_ev
    return new_ins

  @classmethod
  def from_expression(cls, expression: "BaseProbabilityExpression"):
    return expression

  outcome: IOutcome = field(init=False, default=None)

  def __repr__(self) -> str:
    return f"\u2119({self.outcome.__repr__()})"

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
    not_prob.outcome = self.outcome
    return not_prob


class SimpleInvertProbabilityExpression(BaseProbabilityExpression):

  def invert(self):
    default_prob = SimpleProbabilityExpression()
    default_prob.outcome = self.outcome
    return default_prob

  def __repr__(self) -> str:
    return f"\u00AC\u2119({self.outcome.__repr__()})"


class UnconditionalProbabilityExpression(BaseProbabilityExpression):
  base_exp: "UnconditionalProbabilityExpression" = None
  aux_exp: "UnconditionalProbabilityExpression" = None

  def invert(self):
    if type(self) is SimpleProbabilityExpression or type(self) is SimpleInvertProbabilityExpression:
      return super().invert()
    # TODO: Add inversion logic

  def __repr__(self) -> str:
    if self.outcome is not None:
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