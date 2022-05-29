from abc import ABC
from collections import Counter
from copy import copy
import math
from pyfields import field
from typing import Callable, List, Union
from probnode.probability.probability_distribution import ProbabilityDistribution
from probnode.datatype.probability_value import ProbabilityValue
from probnode.probability.event import GenericEvent, GenericSureEvent, BaseEvent, AtomicEvent

from probnode.probability.random_variable import RandomVariable


class AdditiveInverse(ABC):
  pass


class Reciprocal(ABC):
  pass


class ProbabilityMeasureOfEvent:
  """Probability measure

  Returns: 
    Probability measure with specified `random_variable` operating on input `event`

  https://en.wikipedia.org/wiki/Probability_space#Definition
  """

  event: BaseEvent = field(default=None)
  random_var: RandomVariable = field(default=RandomVariable())

  def __init__(self, event: BaseEvent = None, random_variable: RandomVariable = RandomVariable()):
    self.event = event

    if type(random_variable) is RandomVariable:
      self.random_var = random_variable
    elif type(random_variable) is float:
      self.random_var = RandomVariable(ProbabilityDistribution(lambda event: random_variable))

  def __add__(self, other: "ProbabilityMeasureOfEvent"):
    sum = SumP()
    sum.args = [self, other]
    return sum

  def __radd__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot add P object to object of type {type(other)}")
    sum = SumP()
    sum.args = [other, self]
    return sum

  def __sub__(self, other: "ProbabilityMeasureOfEvent"):
    sum = SumP()
    sum.args = [self, AdditiveInverseP.from_P(other)]
    return sum

  def __rsub__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot subtract P object from object of type {type(other)}")
    sum = SumP()
    sum.args = [other, AdditiveInverseP.from_P(self)]
    return sum

  def __neg__(self):
    return self.additive_invert()

  def __mul__(self, other: "ProbabilityMeasureOfEvent"):
    product = ProductP()
    product.args = [self, other]
    return product

  def __rmul__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot multiply P object to object of type {type(other)}")
    product = ProductP()
    product.args = [other, self]
    return product

  def __truediv__(self, other: "ProbabilityMeasureOfEvent"):
    product = ProductP()
    product.args = [self, ReciprocalP.from_P(other)]
    return product

  def __rtruediv__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot divide P object from object of type {type(other)}")
    product = ProductP()
    product.args = [other, ReciprocalP.from_P(self)]
    return product

  def __repr__(self) -> str:
    if type(self.event) is GenericSureEvent:
      return str(float(1))
    return f"\u2119\U00001D6A({self.event.__repr__()})"

  def __eq__(self, __x: object) -> bool:
    return self.__hash__() == __x.__hash__()

  def __ne__(self, __x: object) -> bool:
    return self.__hash__() != __x.__hash__()

  def __hash__(self) -> int:
    return hash(f"{repr(self)}")

  def is_pure_prob_measure(self) -> bool:
    if type(self) is ProbabilityMeasureOfEvent:
      return True
    return False

  def reciprocate(self) -> "ProbabilityMeasureOfEvent":
    if issubclass(type(self), ChainP):
      return ReciprocalChainP.from_P(self)
    return ReciprocalP.from_P(self)

  def additive_invert(self) -> "ProbabilityMeasureOfEvent":
    if issubclass(type(self), ChainP):
      return AdditiveInverseChainP.from_P(self)
    return AdditiveInverseP.from_P(self)


class DerivedP(ProbabilityMeasureOfEvent):
  base: ProbabilityMeasureOfEvent = field(default=None)


class AdditiveInverseP(DerivedP, AdditiveInverse):

  @classmethod
  def from_P(cls, base_prob_measure: ProbabilityMeasureOfEvent) -> ProbabilityMeasureOfEvent:
    if type(base_prob_measure) is AdditiveInverseP:
      return base_prob_measure.base
    inverse = AdditiveInverseP()
    inverse.base = base_prob_measure
    return inverse

  def __init__(self, exp: BaseEvent = None):
    super().__init__(exp)
    self.base = ProbabilityMeasureOfEvent(exp)

  def __repr__(self) -> str:
    return f"- {self.base.__repr__()}"


class ReciprocalP(DerivedP, Reciprocal):

  @classmethod
  def from_P(cls, base_prob_measure: ProbabilityMeasureOfEvent) -> ProbabilityMeasureOfEvent:
    if type(base_prob_measure) is ReciprocalP:
      return base_prob_measure.base
    reciprocal = ReciprocalP()
    reciprocal.base = base_prob_measure
    return reciprocal

  def __init__(self, exp: BaseEvent = None):
    super().__init__(exp)
    self.base = ProbabilityMeasureOfEvent(exp)

  def __repr__(self) -> str:
    return f"1/{self.base.__repr__()}"


class ChainP(ProbabilityMeasureOfEvent):
  args: List[Union[float, ProbabilityMeasureOfEvent]] = field(default=[])

  def is_permutation_of(self, other: "ChainP") -> bool:
    if type(self) is type(other):
      return Counter(self.args) == Counter(other.args)
    return False


class SumP(ChainP):

  def __add__(self, other: Union[float, int, "ProbabilityMeasureOfEvent"]):
    sum = SumP()
    sum.args = copy(self.args)
    sum.args.append(other)
    return sum

  def __radd__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot add SumP object to object of type {type(other)}")
    sum = SumP()
    sum.args = [other, copy(self.args)]
    return sum

  def __sub__(self, other: Union[float, int, "ProbabilityMeasureOfEvent"]):
    sum = SumP()
    sum.args = copy(self.args)
    if isinstance(other, (int, float)):
      sum.args.append(-other)
    elif issubclass(type(other), ChainP):
      sum.args.append(AdditiveInverseChainP.from_P(other))
    else:
      sum.args.append(AdditiveInverseP.from_P(other))
    return sum

  def __repr__(self) -> str:
    rep = ""
    for item in self.args:
      if not issubclass(type(item), AdditiveInverse):
        rep += "+ "
      rep += f"{repr(item)} "
    return rep.strip("+ ")


class AdditiveInverseChainP(ChainP, AdditiveInverseP):

  @classmethod
  def from_P(cls, base_prob_measure: ProbabilityMeasureOfEvent) -> ProbabilityMeasureOfEvent:
    if type(base_prob_measure) is AdditiveInverseChainP:
      return base_prob_measure.base
    inverse = AdditiveInverseChainP()
    inverse.base = base_prob_measure
    return inverse


class ProductP(ChainP):

  def __mul__(self, other: Union[float, int, "ProbabilityMeasureOfEvent"]):
    product = ProductP()
    product.args = copy(self.args)
    product.args.append(other)
    return product

  def __rmul__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot add SumP object to object of type {type(other)}")
    product = ProductP()
    product.args = [other, copy(self.args)]
    return product

  def __truediv__(self, other: Union[float, int, ProbabilityMeasureOfEvent]):
    product = ProductP()
    product.args = copy(self.args)
    if isinstance(other, (int, float)):
      product.args.append(1 / other)
    elif issubclass(type(other), ChainP):
      product.args.append(ReciprocalChainP.from_P(other))
    else:
      product.args.append(ReciprocalP.from_P(other))
    return product

  def __repr__(self) -> str:
    s = ""
    for idx, item in enumerate(self.args):
      if idx != 0:
        s += " * "
      if issubclass(type(item), SumP):
        s += f"({repr(item)})"
      else:
        s += f"{repr(item)}"
    return s


class ReciprocalChainP(ChainP, ReciprocalP):

  @classmethod
  def from_P(cls, base_prob_measure: ProbabilityMeasureOfEvent) -> ProbabilityMeasureOfEvent:
    if type(base_prob_measure) is ReciprocalChainP:
      return base_prob_measure.base
    reciprocal = ReciprocalChainP()
    reciprocal.base = base_prob_measure
    return reciprocal


class ProbabilityMeasure:
  random_variable: field(RandomVariable, default=RandomVariable())

  def __init__(self, random_variable: Union[RandomVariable, float, None] = None) -> None:
    if issubclass(type(random_variable), RandomVariable):
      self.random_variable = random_variable
    elif type(random_variable) is float or random_variable is None:
      self.random_variable = RandomVariable(
          ProbabilityDistribution(lambda event_set: random_variable)
          )
    else:
      raise TypeError(
          f"Cannot assign {type(random_variable)} as {ProbabilityDistribution.__name__}"
          )

  def __call__(self, event: BaseEvent) -> ProbabilityMeasureOfEvent:
    return ProbabilityMeasureOfEvent(event, self.random_variable)

  def __repr__(self) -> str:
    return f"\u2119( {repr(self.random_variable)} )"


def P__(random_variable: Union[RandomVariable, float, None] = None) -> ProbabilityMeasure:
  """Prototyping probability measure `\u2119: \U00002131 -> [0,1]`

  Returns: 
    Probability measure prototype with specified random variable function
  
  Usage:
  ```
    p_x = P__(random_variable) # A Random variable which has probability function operating on the event set
    eval(p_x(event_set))
  ```

  https://en.wikipedia.org/wiki/Probability_space#Definition
  """
  return ProbabilityMeasure(random_variable)
