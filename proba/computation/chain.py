from typing import List

from proba.interface.iProbabilityExpression import IProbabilityExpression
from proba.probability import BaseProbabilityExpression


class Node(float):
  exp: BaseProbabilityExpression

  def __new__(cls, exp: BaseProbabilityExpression = None, value: float = 0):
    return super().__new__(cls, value)

  def __init__(self, exp: BaseProbabilityExpression = None, value: float = 0):
    float.__init__(value)
    self.exp = exp

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
    return f"[{self.exp.__repr__()}]"


class DerivedNode(Node):
  base: Node


class AdditiveInverseNode(DerivedNode):

  @classmethod
  def from_node(cls, base_node: Node) -> Node:
    if type(base_node) is AdditiveInverseNode:
      return base_node.base
    inverse = AdditiveInverseNode()
    inverse.base = base_node
    return inverse

  def __repr__(self) -> str:
    return f"(-){self.base.__repr__()}"


class ReciprocalNode(DerivedNode):

  @classmethod
  def from_node(cls, base_node: Node) -> Node:
    if type(base_node) is ReciprocalNode:
      return base_node.base
    reciproc = ReciprocalNode()
    reciproc.base = base_node
    return reciproc

  def __repr__(self) -> str:
    return f"1/{self.base.__repr__()}"


class ChainNode(Node):
  args: List[Node]


class SumNode(ChainNode):

  def __add__(self, other: "Node"):
    self.args.append(other)
    return self

  def __sub__(self, other: "Node"):
    self.args.append(AdditiveInverseNode.from_node(other))
    return self

  def __repr__(self) -> str:
    return " + ".join(repr(item) for item in self.args)


class ProductNode(ChainNode):

  def __mul__(self, other: "Node"):
    self.args.append(other)
    return self

  def __truediv__(self, other: "Node"):
    self.args.append(ReciprocalNode.from_node(other))
    return self

  def __repr__(self) -> str:
    return " * ".join(repr(item) for item in self.args)