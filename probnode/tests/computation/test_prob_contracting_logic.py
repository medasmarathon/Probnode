from probnode import *
from probnode.probability import *
from probnode.probability.probability_measure import *
from probnode.computation.probability_contracting_logic import *
from typing import List
import pytest


@pytest.mark.parametrize(
    ("input", "expect"),
    [([p__X_(ES__(Outcome("sample"))),
       AdditiveInverseP(ES__(Outcome("sample")))], ProbabilityMeasure(None, 0)),
     ([
         p__X_(ES__(Outcome("sample1"))) + p__X_(ES__(Outcome("sample2"))),
         AdditiveInverseChainP.
         from_P(p__X_(ES__(Outcome("sample1"))) + p__X_(ES__(Outcome("sample2"))))
         ], ProbabilityMeasure(None, 0))]
    )
def test_contract_sum_2_nodes(input: List[ProbabilityMeasure], expect: ProbabilityMeasure):
  assert try_contract_sum_2_nodes(input) == expect


@pytest.mark.parametrize(("input", "expect"), [
    ([p__X_(ES__(Outcome("sample"))),
      ReciprocalP(ES__(Outcome("sample")))], ProbabilityMeasure(None, 1)),
    ([
        p__X_(ES__(Outcome("sample1")) & ES__(Outcome("sample2"))),
        ReciprocalP.from_P(p__X_(ES__(Outcome("sample2"))))
        ], p__X_(ES__(Outcome("sample1")) // ES__(Outcome("sample2")))),
    ([p__X_(ES__(Outcome("sample1"))),
      p__X_(ES__(Outcome("sample2")))], p__X_(ES__(Outcome("sample1")) & ES__(Outcome("sample2"))))
    ])
def test_contract_product_2_nodes(input: List[ProbabilityMeasure], expect: ProbabilityMeasure):
  assert contract_product_2_nodes(input) == expect


def test_is_or_probability_pattern():
  assert is_or_probability_pattern(
      p__X_(ES__(Outcome("x"))), p__X_(ES__(Outcome("y"))),
      p__X_(ES__(Outcome("x")) & ES__(Outcome("y"))).additive_invert()
      ) == True
  assert is_or_probability_pattern(
      p__X_(ES__(Outcome("x"))), p__X_(ES__(Outcome("yyyy"))),
      p__X_(ES__(Outcome("x")) & ES__(Outcome("y"))).additive_invert()
      ) == False
  assert is_or_probability_pattern(
      p__X_(ES__(Outcome("x"))), p__X_(ES__(Outcome("yyyy"))),
      p__X_(ES__(Outcome("x")) & ES__(Outcome("y")))
      ) == False


def test_try_contract_or_probability_pattern():
  assert try_contract_or_probability_pattern(
      p__X_(ES__(Outcome("x"))), p__X_(ES__(Outcome("y"))),
      p__X_(ES__(Outcome("x")) & ES__(Outcome("y"))).additive_invert()
      ) == p__X_(ES__(Outcome("x")) | ES__(Outcome("y")))
  assert try_contract_or_probability_pattern(
      p__X_(ES__(Outcome("x"))), p__X_(ES__(Outcome("yyyy"))),
      p__X_(ES__(Outcome("x")) & ES__(Outcome("y"))).additive_invert()
      ) == None
  assert try_contract_or_probability_pattern(
      p__X_(ES__(Outcome("x"))), p__X_(ES__(Outcome("yyyy"))),
      p__X_(ES__(Outcome("x")) & ES__(Outcome("y")))
      ) == None


def test_contract_sum_3_nodes():
  assert contract_sum_3_nodes([
      p__X_(ES__(Outcome("x"))),
      p__X_(ES__(Outcome("y"))),
      p__X_(ES__(Outcome("x")) & ES__(Outcome("y"))).additive_invert()
      ]) == p__X_(ES__(Outcome("x")) | ES__(Outcome("y")))
  assert contract_sum_3_nodes([
      p__X_(ES__(Outcome("x"))),
      p__X_(ES__(Outcome("yyyy"))),
      p__X_(ES__(Outcome("x")) & ES__(Outcome("y"))).additive_invert()
      ]) == None
  assert contract_sum_3_nodes([
      p__X_(ES__(Outcome("x"))),
      p__X_(ES__(Outcome("yyyy"))),
      p__X_(ES__(Outcome("x")) & ES__(Outcome("y")))
      ]) == None
