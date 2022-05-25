from abc import ABC
from collections import Counter
from copy import copy
import math
from pyfields import field
from typing import Callable, List, Union
from probability_distribution import ProbabilityDistribution
from probnode.datatype.probability_value import ProbabilityValue
from probnode.probability.event import GenericEvent, GenericSureEvent, BaseEvent, AtomicEvent

from probnode.probability.random_variable import RandomVariable


class AdditiveInverse(ABC):
  pass


class Reciprocal(ABC):
  pass


class ProbabilityMeasure:
  """Probability measure

  Returns: 
    Probability measure with specified `random_variable_function` operating on input `event_set`

  https://en.wikipedia.org/wiki/Probability_space#Definition
  """

  _value: Union[ProbabilityValue, None] = field(default=None)

  @property
  def value(self) -> ProbabilityValue:
    return self._value if self._value is not None else self.random_var(self.event)

  @value.setter
  def value(self, value: Union[float, Callable, None]):
    if self.event is not None and type(self.event.outcome) == GenericSureEvent:
      raise ValueError(f"Cannot assign value for EventSet of {GenericSureEvent.__name__}")

    if value is not None:
      self._value = ProbabilityValue(value)
    else:
      self._value = None

  event: BaseEvent = field(default=None)
  random_var: RandomVariable = field(default=RandomVariable())

  def __init__(self, event: BaseEvent = None, random_variable: RandomVariable = RandomVariable()):
    self.event = event

    if type(random_variable) is RandomVariable:
      self.random_var = random_variable
    elif type(random_variable) is float:
      self.random_var = RandomVariable(ProbabilityDistribution(lambda event: random_variable))

    self._value = self.random_var(event) if event is not None else None
    if event is not None and type(event) == GenericSureEvent:
      self._value = 1

  def __add__(self, other: "ProbabilityMeasure"):
    sum = SumP()
    sum.args = [self, other]
    return sum

  def __radd__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot add P object to object of type {type(other)}")
    sum = SumP()
    sum.args = [other, self]
    return sum

  def __sub__(self, other: "ProbabilityMeasure"):
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

  def __mul__(self, other: "ProbabilityMeasure"):
    product = ProductP()
    product.args = [self, other]
    return product

  def __rmul__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot multiply P object to object of type {type(other)}")
    product = ProductP()
    product.args = [other, self]
    return product

  def __truediv__(self, other: "ProbabilityMeasure"):
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
    if self.event is None:
      return str(self.value)
    return f"\u2119\U00001D6A({self.event.__repr__()})"

  def __eq__(self, __x: object) -> bool:
    return self.__hash__() == __x.__hash__()

  def __ne__(self, __x: object) -> bool:
    return self.__hash__() != __x.__hash__()

  def __hash__(self) -> int:
    return hash(f"{repr(self)} = {self.value}")

  def is_pure_prob_measure(self) -> bool:
    if type(self) in [ProbabilityMeasure, ProbabilityMeasure]:
      return True
    return False

  def reciprocate(self) -> "ProbabilityMeasure":
    if issubclass(type(self), ChainP):
      return ReciprocalChainP.from_P(self)
    return ReciprocalP.from_P(self)

  def additive_invert(self) -> "ProbabilityMeasure":
    if issubclass(type(self), ChainP):
      return AdditiveInverseChainP.from_P(self)
    return AdditiveInverseP.from_P(self)


class DerivedP(ProbabilityMeasure):
  base: ProbabilityMeasure = field(default=None)
  _derived_value: Union[float, None] = field(default=None)

  @ProbabilityMeasure.value.getter
  def value(self) -> Union[float, None]:
    if self.derived_value is not None:
      return self.derived_value
    return None

  @property
  def derived_value(self) -> Union[float, None]:
    return self._derived_value

  @derived_value.setter
  def derived_value(self, derived_value: Union[float, None]):
    self._derived_value = derived_value


class AdditiveInverseP(DerivedP, AdditiveInverse):

  @DerivedP.derived_value.getter
  def derived_value(self) -> Union[float, None]:
    if self.base.value is not None:
      return 0 - float(self.base.value)
    return self._derived_value if self._derived_value is not None else None

  @classmethod
  def from_P(cls, base_prob_measure: ProbabilityMeasure) -> ProbabilityMeasure:
    if type(base_prob_measure) is AdditiveInverseP:
      return base_prob_measure.base
    inverse = AdditiveInverseP()
    inverse.base = base_prob_measure
    return inverse

  def __init__(self, exp: BaseEvent = None):
    super().__init__(exp)
    self.base = ProbabilityMeasure(exp)

  def __repr__(self) -> str:
    return f"- {self.base.__repr__()}"


class ReciprocalP(DerivedP, Reciprocal):

  @DerivedP.derived_value.getter
  def derived_value(self) -> Union[float, None]:
    if self.base.value is not None and self.base.value != 0:
      return 1 / float(self.base.value)
    return self._derived_value if self._derived_value is not None else None

  @classmethod
  def from_P(cls, base_prob_measure: ProbabilityMeasure) -> ProbabilityMeasure:
    if type(base_prob_measure) is ReciprocalP:
      return base_prob_measure.base
    reciprocal = ReciprocalP()
    reciprocal.base = base_prob_measure
    return reciprocal

  def __init__(self, exp: BaseEvent = None):
    super().__init__(exp)
    self.base = ProbabilityMeasure(exp)

  def __repr__(self) -> str:
    return f"1/{self.base.__repr__()}"


class ChainP(ProbabilityMeasure):
  args: List[Union[float, ProbabilityMeasure]] = field(default=[])
  _chain_value: Union[float, None] = field(default=None)

  @ProbabilityMeasure.value.getter
  def value(self) -> Union[float, None]:
    if self.chain_value is not None:
      return self.chain_value
    return self._value

  @property
  def chain_value(self) -> float:
    """If all chain members' value are defined (not `None`), then return calculated value from chain members
      Else return the designated value or the default value for this `ChainP`

    Returns:
        float: Calculated value
    """
    return self._chain_value

  @chain_value.setter
  def chain_value(self, chain_value: float):
    self._chain_value = chain_value

  def _get_value_of_chain_item(self, item: Union[float, ProbabilityMeasure]) -> Union[float, None]:
    if isinstance(item, (int, float)):
      return item
    else:
      return float(item.value) if item.value is not None else None

  def is_permutation_of(self, other: "ChainP") -> bool:
    if type(self) is type(other):
      return Counter(self.args) == Counter(other.args)
    return False


class SumP(ChainP):

  @ChainP.chain_value.getter
  def chain_value(self) -> float:
    if None in list(map(lambda x: self._get_value_of_chain_item(x), self.args)):
      return self._chain_value
    return sum(list(map(lambda x: float(x.value), self.args)))

  def __add__(self, other: Union[float, int, "ProbabilityMeasure"]):
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

  def __sub__(self, other: Union[float, int, "ProbabilityMeasure"]):
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
  def from_P(cls, base_prob_measure: ProbabilityMeasure) -> ProbabilityMeasure:
    if type(base_prob_measure) is AdditiveInverseChainP:
      return base_prob_measure.base
    inverse = AdditiveInverseChainP()
    inverse.base = base_prob_measure
    return inverse

  @ProbabilityMeasure.value.getter
  def value(self) -> Union[float, None]:
    if self.derived_value is not None:
      return self.derived_value
    return None


class ProductP(ChainP):

  @ChainP.chain_value.getter
  def chain_value(self) -> Union[float, None]:
    if len(self.args) == 0:
      return 1.0
    if None in list(map(lambda x: self._get_value_of_chain_item(x), self.args)):
      return self._chain_value
    return math.prod(list(map(lambda x: float(x.value), self.args)))

  def __mul__(self, other: Union[float, int, "ProbabilityMeasure"]):
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

  def __truediv__(self, other: Union[float, int, ProbabilityMeasure]):
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
  def from_P(cls, base_prob_measure: ProbabilityMeasure) -> ProbabilityMeasure:
    if type(base_prob_measure) is ReciprocalChainP:
      return base_prob_measure.base
    reciprocal = ReciprocalChainP()
    reciprocal.base = base_prob_measure
    return reciprocal

  @ProbabilityMeasure.value.getter
  def value(self) -> Union[float, None]:
    if self.derived_value is not None:
      return self.derived_value
    return None


class ProbabilityMeasureWithRandomVariableFactory:
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

  def __call__(self, event: BaseEvent) -> ProbabilityMeasure:
    return ProbabilityMeasure(event, self.random_variable)

  def __repr__(self) -> str:
    return f"\u2119( {repr(self.random_variable)} )"


def P__(
    random_variable: Union[RandomVariable, float, None] = None
    ) -> ProbabilityMeasureWithRandomVariableFactory:
  """Prototyping probability measure `\u2119: \U00002131 -> [0,1]`

  Returns: 
    Probability measure prototype with specified random variable function
  
  Usage:
  ```
    p_x = P__(random_variable) # A Random variable which has probability function operating on the event set
    p_x(event_set).value
  ```

  https://en.wikipedia.org/wiki/Probability_space#Definition
  """
  return ProbabilityMeasureWithRandomVariableFactory(random_variable)
