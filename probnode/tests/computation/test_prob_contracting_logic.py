from probnode import *
from probnode.probability import *
from probnode.probability.probability_measure import *
from probnode.computation.probability_contracting_logic import *
from typing import List
import pytest


@pytest.mark.parametrize(("input", "expect"),
                         [([
                             ProbabilityMeasureOfEvent(Event(Outcome("sample"))),
                             AdditiveInverseP(Event(Outcome("sample")))
                             ], ProbabilityMeasureOfEvent(None, 0)),
                          ([
                              ProbabilityMeasureOfEvent(Event(Outcome("sample1"))) +
                              ProbabilityMeasureOfEvent(Event(Outcome("sample2"))),
                              AdditiveInverseChainP.from_P(
                                  ProbabilityMeasureOfEvent(Event(Outcome("sample1"))) +
                                  ProbabilityMeasureOfEvent(Event(Outcome("sample2")))
                                  )
                              ], ProbabilityMeasureOfEvent(None, 0))])
def test_try_contract_sum_2_Ps(
        input: List[ProbabilityMeasureOfEvent], expect: ProbabilityMeasureOfEvent
    ):
    assert try_contract_sum_2_Ps(input) == expect


@pytest.mark.parametrize(
    ("input", "expect"),
    [([ProbabilityMeasureOfEvent(Event(Outcome("sample"))),
       ReciprocalP(Event(Outcome("sample")))], ProbabilityMeasureOfEvent(None, 1)),
     ([
         ProbabilityMeasureOfEvent(Event(Outcome("sample1")) & Event(Outcome("sample2"))),
         ReciprocalP.from_P(ProbabilityMeasureOfEvent(Event(Outcome("sample2"))))
         ], ProbabilityMeasureOfEvent(Event(Outcome("sample1")) // Event(Outcome("sample2")))),
     ([
         ProbabilityMeasureOfEvent(Event(Outcome("sample1"))),
         ProbabilityMeasureOfEvent(Event(Outcome("sample2")))
         ], ProbabilityMeasureOfEvent(Event(Outcome("sample1")) & Event(Outcome("sample2"))))]
    )
def test_contract_product_2_Ps(
        input: List[ProbabilityMeasureOfEvent], expect: ProbabilityMeasureOfEvent
    ):
    assert contract_product_2_Ps(input) == expect


def test_is_OrEvent_pattern():
    assert is_OrEvent_pattern(
        ProbabilityMeasureOfEvent(Event(Outcome("x"))),
        ProbabilityMeasureOfEvent(Event(Outcome("y"))),
        ProbabilityMeasureOfEvent(Event(Outcome("x"))
                                  & Event(Outcome("y"))).additive_invert()
        ) == True
    assert is_OrEvent_pattern(
        ProbabilityMeasureOfEvent(Event(Outcome("x"))),
        ProbabilityMeasureOfEvent(Event(Outcome("yyyy"))),
        ProbabilityMeasureOfEvent(Event(Outcome("x"))
                                  & Event(Outcome("y"))).additive_invert()
        ) == False
    assert is_OrEvent_pattern(
        ProbabilityMeasureOfEvent(Event(Outcome("x"))),
        ProbabilityMeasureOfEvent(Event(Outcome("yyyy"))),
        ProbabilityMeasureOfEvent(Event(Outcome("x")) & Event(Outcome("y")))
        ) == False


def test_try_contract_OrEvent_pattern():
    assert try_contract_OrEvent_pattern(
        ProbabilityMeasureOfEvent(Event(Outcome("x"))),
        ProbabilityMeasureOfEvent(Event(Outcome("y"))),
        ProbabilityMeasureOfEvent(Event(Outcome("x"))
                                  & Event(Outcome("y"))).additive_invert()
        ) == ProbabilityMeasureOfEvent(Event(Outcome("x")) | Event(Outcome("y")))
    assert try_contract_OrEvent_pattern(
        ProbabilityMeasureOfEvent(Event(Outcome("x"))),
        ProbabilityMeasureOfEvent(Event(Outcome("yyyy"))),
        ProbabilityMeasureOfEvent(Event(Outcome("x"))
                                  & Event(Outcome("y"))).additive_invert()
        ) == None
    assert try_contract_OrEvent_pattern(
        ProbabilityMeasureOfEvent(Event(Outcome("x"))),
        ProbabilityMeasureOfEvent(Event(Outcome("yyyy"))),
        ProbabilityMeasureOfEvent(Event(Outcome("x")) & Event(Outcome("y")))
        ) == None


def test_contract_sum_3_Ps():
    assert contract_sum_3_Ps([
        ProbabilityMeasureOfEvent(Event(Outcome("x"))),
        ProbabilityMeasureOfEvent(Event(Outcome("y"))),
        ProbabilityMeasureOfEvent(Event(Outcome("x"))
                                  & Event(Outcome("y"))).additive_invert()
        ]) == ProbabilityMeasureOfEvent(Event(Outcome("x")) | Event(Outcome("y")))
    assert contract_sum_3_Ps([
        ProbabilityMeasureOfEvent(Event(Outcome("x"))),
        ProbabilityMeasureOfEvent(Event(Outcome("yyyy"))),
        ProbabilityMeasureOfEvent(Event(Outcome("x"))
                                  & Event(Outcome("y"))).additive_invert()
        ]) == None
    assert contract_sum_3_Ps([
        ProbabilityMeasureOfEvent(Event(Outcome("x"))),
        ProbabilityMeasureOfEvent(Event(Outcome("yyyy"))),
        ProbabilityMeasureOfEvent(Event(Outcome("x")) & Event(Outcome("y")))
        ]) == None
