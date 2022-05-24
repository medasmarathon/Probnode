from probnode import *
from probnode.probability import *
from probnode.probability.probability_measure import *
from probnode.computation.probability_contracting_logic import *
from typing import List
import pytest


@pytest.mark.parametrize(("input", "expect"),
                         [([
                             ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample"))),
                             AdditiveInverseP(Event(Outcome("sample")))
                             ], ProbabilityMeasure(None, 0)),
                          ([
                              ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample1"))) +
                              ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample2"))),
                              AdditiveInverseChainP.from_P(
                                  ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample1"))) +
                                  ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample2")))
                                  )
                              ], ProbabilityMeasure(None, 0))])
def test_try_contract_sum_2_Ps(input: List[ProbabilityMeasure], expect: ProbabilityMeasure):
  assert try_contract_sum_2_Ps(input) == expect


@pytest.mark.parametrize(
    ("input", "expect"),
    [([
        ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample"))),
        ReciprocalP(Event(Outcome("sample")))
        ], ProbabilityMeasure(None, 1)),
     ([
         ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample1")) & Event(Outcome("sample2"))),
         ReciprocalP.from_P(ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample2"))))
         ],
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample1")) // Event(Outcome("sample2")))),
     ([
         ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample1"))),
         ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample2")))
         ],
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("sample1")) & Event(Outcome("sample2"))))]
    )
def test_contract_product_2_Ps(input: List[ProbabilityMeasure], expect: ProbabilityMeasure):
  assert contract_product_2_Ps(input) == expect


def test_is_OrEvent_pattern():
  assert is_OrEvent_pattern(
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("y"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))
                                          & Event(Outcome("y"))).additive_invert()
      ) == True
  assert is_OrEvent_pattern(
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("yyyy"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))
                                          & Event(Outcome("y"))).additive_invert()
      ) == False
  assert is_OrEvent_pattern(
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("yyyy"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x")) & Event(Outcome("y")))
      ) == False


def test_try_contract_OrEvent_pattern():
  assert try_contract_OrEvent_pattern(
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("y"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))
                                          & Event(Outcome("y"))).additive_invert()
      ) == ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x")) | Event(Outcome("y")))
  assert try_contract_OrEvent_pattern(
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("yyyy"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))
                                          & Event(Outcome("y"))).additive_invert()
      ) == None
  assert try_contract_OrEvent_pattern(
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("yyyy"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x")) & Event(Outcome("y")))
      ) == None


def test_contract_sum_3_Ps():
  assert contract_sum_3_Ps([
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("y"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))
                                          & Event(Outcome("y"))).additive_invert()
      ]) == ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x")) | Event(Outcome("y")))
  assert contract_sum_3_Ps([
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("yyyy"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))
                                          & Event(Outcome("y"))).additive_invert()
      ]) == None
  assert contract_sum_3_Ps([
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("yyyy"))),
      ProbMeasure_with_RandomVar_on_Event(Event(Outcome("x")) & Event(Outcome("y")))
      ]) == None
