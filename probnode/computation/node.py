from abc import ABC
from copy import copy
from typing import List
from probnode.datatype.probabilityvalue import ProbabilityValue
from probnode.probability.event import SureEvent

from probnode.interface.iprobability_expression import IProbabilityExpression
from probnode.probability.probability import BaseProbabilityExpression, SimpleProbabilityExpression


class AdditiveInverse(ABC):
  pass


class Reciprocal(ABC):
  pass


class Node(float):
  value: ProbabilityValue
  exp: BaseProbabilityExpression

  def __new__(cls, exp: BaseProbabilityExpression = None, value: float = 0):
    return super().__new__(cls, value)

  def __init__(self, exp: BaseProbabilityExpression = None, value: float = 0):
    float.__init__(value)
    self.exp = exp
    self.value = ProbabilityValue(value)

  def __add__(self, other: "Node"):
    sum = SumNode()
    sum.args = [self, other]
    return sum

  def __sub__(self, other: "Node"):
    sum = SumNode()
    sum.args = [self, AdditiveInverseNode.from_node(other)]
    return sum

  def __mul__(self, other: "Node"):
    product = ProductNode()
    product.args = [self, other]
    return product

  def __truediv__(self, other: "Node"):
    product = ProductNode()
    product.args = [self, ReciprocalNode.from_node(other)]
    return product

  def __repr__(self) -> str:
    if type(self.exp) is SimpleProbabilityExpression and type(self.exp.event) is SureEvent:
      return "1"
    if self.exp is None:
      return str(self.value)
    return f"[{self.exp.__repr__()}]"

  def __eq__(self, __x: object) -> bool:
    return repr(self) == repr(__x)

  def __ne__(self, __x: object) -> bool:
    return repr(self) != repr(__x)

  def __hash__(self) -> int:
    return hash(f"{repr(self)} = {self.value}")


class DerivedNode(Node):
  base: Node


class AdditiveInverseNode(DerivedNode, AdditiveInverse):

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
  args: List[Node] = []


class SumNode(ChainNode):

  def __add__(self, other: "Node"):
    sum = SumNode()
    sum.args = copy(self.args)
    sum.args.append(other)
    return sum

  def __sub__(self, other: "Node"):
    sum = SumNode()
    sum.args = copy(self.args)
    if issubclass(type(other), ChainNode):
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


class AdditiveInverseChainNode(AdditiveInverseNode, ChainNode):

  @classmethod
  def from_node(cls, base_node: Node) -> Node:
    if type(base_node) is AdditiveInverseChainNode:
      return base_node.base
    inverse = AdditiveInverseChainNode()
    inverse.base = base_node
    return inverse


class ProductNode(ChainNode):

  def __mul__(self, other: "Node"):
    product = ProductNode()
    product.args = copy(self.args)
    product.args.append(other)
    return product

  def __truediv__(self, other: "Node"):
    product = ProductNode()
    product.args = copy(self.args)
    if issubclass(type(other), ChainNode):
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


class ReciprocalChainNode(ReciprocalNode, ChainNode):

  @classmethod
  def from_node(cls, base_node: Node) -> Node:
    if type(base_node) is ReciprocalChainNode:
      return base_node.base
    reciprocal = ReciprocalChainNode()
    reciprocal.base = base_node
    return reciprocal


class N(Node):
  pass