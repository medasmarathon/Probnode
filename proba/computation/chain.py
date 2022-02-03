from typing import List

from proba.interface.iProbabilityExpression import IProbabilityExpression
from proba.probability import BaseProbabilityExpression


class Node:
  exp: BaseProbabilityExpression

  def __init__(self, exp: BaseProbabilityExpression = None):
    self.exp = exp

  def __add__(self, other: "Node"):
    sum = SumNode()
    sum.args = [self, other]
    return sum

  def __sub__(self, other: "Node"):
    sum = SumNode()
    sum.args = [self, NegativeNode.from_node(other)]
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


class NegativeNode(Node):
  base: Node

  @classmethod
  def from_node(cls, base_node: Node) -> Node:
    if type(base_node) is NegativeNode:
      return Node(base_node.exp)
    neg = NegativeNode()
    neg.base = base_node
    return neg

  def __repr__(self) -> str:
    return f"[- {self.base.__repr__()}]"


class ReciprocalNode(Node):
  base: Node

  @classmethod
  def from_node(cls, base_node: Node) -> Node:
    if type(base_node) is ReciprocalNode:
      return Node(base_node.exp)
    reciproc = ReciprocalNode()
    reciproc.base = base_node
    return reciproc

  def __repr__(self) -> str:
    return f"[1 / {self.base.__repr__()}]"


class SumNode(Node):
  args: List[Node]

  def __add__(self, other: "Node"):
    self.args.append(other)
    return self

  def __sub__(self, other: "Node"):
    self.args.append(NegativeNode.from_node(other))
    return self

  def __repr__(self) -> str:
    return " + ".join(repr(item) for item in self.args)


class ProductNode(Node):
  args: List[Node]

  def __mul__(self, other: "Node"):
    self.args.append(other)
    return self

  def __truediv__(self, other: "Node"):
    self.args.append(ReciprocalNode.from_node(other))
    return self

  def __repr__(self) -> str:
    return " * ".join(repr(item) for item in self.args)