from abc import ABC
from collections import Counter
from copy import copy
import math
from typing import List, Union
from probnode.datatype.probabilityvalue import ProbabilityValue
from probnode.probability.event import SureEvent

from probnode.interface.iprobability_expression import IProbabilityExpression
from probnode.probability.probability import BaseProbabilityExpression, SimpleProbabilityExpression


class AdditiveInverse(ABC):
  pass


class Reciprocal(ABC):
  pass


class Node:
  _value: Union[ProbabilityValue, None] = None

  @property
  def value(self) -> ProbabilityValue:
    if self.exp is not None:
      return self.exp.value
    return self._value

  @value.setter
  def value(self, value: float):
    if self.exp is not None and type(self.exp.event) == SureEvent:
      raise ValueError("Cannot assign value for probability of SureEvent")
    self._value = ProbabilityValue(value) if value is not None else None

  exp: BaseProbabilityExpression

  def __init__(self, exp: BaseProbabilityExpression = None, value: Union[float, None] = None):
    self.exp = exp
    if exp is not None and type(exp.event) == SureEvent:
      self._value = 1
    else:
      self.value = ProbabilityValue(value) if value is not None else None

  def __add__(self, other: "Node"):
    sum = SumNode()
    sum.args = [self, other]
    return sum

  def __radd__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot add Node object to object of type {type(other)}")
    sum = SumNode()
    sum.args = [other, self]
    return sum

  def __sub__(self, other: "Node"):
    sum = SumNode()
    sum.args = [self, AdditiveInverseNode.from_node(other)]
    return sum

  def __rsub__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot subtract Node object from object of type {type(other)}")
    sum = SumNode()
    sum.args = [other, AdditiveInverseNode.from_node(self)]
    return sum

  def __mul__(self, other: "Node"):
    product = ProductNode()
    product.args = [self, other]
    return product

  def __rmul__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot multiply Node object to object of type {type(other)}")
    product = ProductNode()
    product.args = [other, self]
    return product

  def __truediv__(self, other: "Node"):
    product = ProductNode()
    product.args = [self, ReciprocalNode.from_node(other)]
    return product

  def __rtruediv__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot divide Node object from object of type {type(other)}")
    product = ProductNode()
    product.args = [other, ReciprocalNode.from_node(self)]
    return product

  def __repr__(self) -> str:
    if type(self.exp) is SimpleProbabilityExpression and type(self.exp.event) is SureEvent:
      return str(float(1))
    if self.exp is None:
      return str(self.value)
    return f"[{self.exp.__repr__()}]"

  def __eq__(self, __x: object) -> bool:
    return self.__hash__() == __x.__hash__()

  def __ne__(self, __x: object) -> bool:
    return self.__hash__() != __x.__hash__()

  def __hash__(self) -> int:
    return hash(f"{repr(self)} = {self.value}")

  def is_pure_node(self) -> bool:
    if type(self) in [Node, N]:
      return True
    return False

  def reciprocate(self) -> "Node":
    if issubclass(type(self), ChainNode):
      return ReciprocalChainNode.from_node(self)
    return ReciprocalNode.from_node(self)

  def additive_invert(self) -> "Node":
    if issubclass(type(self), ChainNode):
      return AdditiveInverseChainNode.from_node(self)
    return AdditiveInverseNode.from_node(self)


class DerivedNode(Node):
  base: Node
  _derived_value: Union[float, None] = None

  @Node.value.getter
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


class AdditiveInverseNode(DerivedNode, AdditiveInverse):

  @DerivedNode.derived_value.getter
  def derived_value(self) -> Union[float, None]:
    if self.base.value is not None:
      return 0 - float(self.base.value)
    return self._derived_value if self._derived_value is not None else None

  @classmethod
  def from_node(cls, base_node: Node) -> Node:
    if type(base_node) is AdditiveInverseNode:
      return base_node.base
    inverse = AdditiveInverseNode()
    inverse.base = base_node
    return inverse

  def __init__(self, exp: BaseProbabilityExpression = None):
    super().__init__(exp)
    self.base = Node(exp)

  def __repr__(self) -> str:
    return f"- {self.base.__repr__()}"


class ReciprocalNode(DerivedNode, Reciprocal):

  @DerivedNode.derived_value.getter
  def derived_value(self) -> Union[float, None]:
    if self.base.value is not None and self.base.value != 0:
      return 1 / float(self.base.value)
    return self._derived_value if self._derived_value is not None else None

  @classmethod
  def from_node(cls, base_node: Node) -> Node:
    if type(base_node) is ReciprocalNode:
      return base_node.base
    reciprocal = ReciprocalNode()
    reciprocal.base = base_node
    return reciprocal

  def __init__(self, exp: BaseProbabilityExpression = None):
    super().__init__(exp)
    self.base = Node(exp)

  def __repr__(self) -> str:
    return f"1/{self.base.__repr__()}"


class ChainNode(Node):
  args: List[Union[float, Node]] = []
  _chain_value: Union[float, None] = None

  @Node.value.getter
  def value(self) -> Union[float, None]:
    if self.chain_value is not None:
      return self.chain_value
    return self._value

  @property
  def chain_value(self) -> float:
    return self._chain_value

  @chain_value.setter
  def chain_value(self, chain_value: float):
    self._chain_value = chain_value

  def _get_value_of_chain_item(self, item: Union[float, Node]) -> Union[float, None]:
    if isinstance(item, (int, float)):
      return item
    else:
      return float(item.value) if item.value is not None else None

  def is_permutation_of(self, other: "ChainNode") -> bool:
    if type(self) is type(other):
      return Counter(self.args) == Counter(other.args)
    return False


class SumNode(ChainNode):

  @ChainNode.chain_value.getter
  def chain_value(self) -> float:
    if None in list(map(lambda x: self._get_value_of_chain_item(x), self.args)):
      return self._chain_value
    return sum(list(map(lambda x: float(x.value), self.args)))

  def __add__(self, other: Union[float, int, "Node"]):
    sum = SumNode()
    sum.args = copy(self.args)
    sum.args.append(other)
    return sum

  def __radd__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot add SumNode object to object of type {type(other)}")
    sum = SumNode()
    sum.args = [other, copy(self.args)]
    return sum

  def __sub__(self, other: Union[float, int, "Node"]):
    sum = SumNode()
    sum.args = copy(self.args)
    if isinstance(other, (int, float)):
      sum.args.append(-other)
    elif issubclass(type(other), ChainNode):
      sum.args.append(AdditiveInverseChainNode.from_node(other))
    else:
      sum.args.append(AdditiveInverseNode.from_node(other))
    return sum

  def __repr__(self) -> str:
    rep = ""
    for item in self.args:
      if not issubclass(type(item), AdditiveInverse):
        rep += "+ "
      rep += f"{repr(item)} "
    return rep.strip("+ ")


class AdditiveInverseChainNode(ChainNode, AdditiveInverseNode):

  @classmethod
  def from_node(cls, base_node: Node) -> Node:
    if type(base_node) is AdditiveInverseChainNode:
      return base_node.base
    inverse = AdditiveInverseChainNode()
    inverse.base = base_node
    return inverse

  @Node.value.getter
  def value(self) -> Union[float, None]:
    if self.derived_value is not None:
      return self.derived_value
    return None


class ProductNode(ChainNode):

  @ChainNode.chain_value.getter
  def chain_value(self) -> Union[float, None]:
    if None in list(map(lambda x: self._get_value_of_chain_item(x), self.args)):
      return self._chain_value
    return math.prod(list(map(lambda x: float(x.value), self.args)))

  def __mul__(self, other: Union[float, int, "Node"]):
    product = ProductNode()
    product.args = copy(self.args)
    product.args.append(other)
    return product

  def __rmul__(self, other: Union[float, int]):
    if not isinstance(other, (int, float)):
      raise TypeError(f"Cannot add SumNode object to object of type {type(other)}")
    product = ProductNode()
    product.args = [other, copy(self.args)]
    return product

  def __truediv__(self, other: Union[float, int, Node]):
    product = ProductNode()
    product.args = copy(self.args)
    if isinstance(other, (int, float)):
      product.args.append(1 / other)
    elif issubclass(type(other), ChainNode):
      product.args.append(ReciprocalChainNode.from_node(other))
    else:
      product.args.append(ReciprocalNode.from_node(other))
    return product

  def __repr__(self) -> str:
    s = ""
    for idx, item in enumerate(self.args):
      if idx != 0:
        s += " * "
      if issubclass(type(item), SumNode):
        s += f"({repr(item)})"
      else:
        s += f"{repr(item)}"
    return s


class ReciprocalChainNode(ChainNode, ReciprocalNode):

  @classmethod
  def from_node(cls, base_node: Node) -> Node:
    if type(base_node) is ReciprocalChainNode:
      return base_node.base
    reciprocal = ReciprocalChainNode()
    reciprocal.base = base_node
    return reciprocal

  @Node.value.getter
  def value(self) -> Union[float, None]:
    if self.derived_value is not None:
      return self.derived_value
    return None


def N(expression: BaseProbabilityExpression, value: float = 0) -> Node:
  return Node(expression, value)