from probnode import Outcome, DiscreteOutcome


def test_simple_outcome_equality():
    outcome_head = Outcome("Head")
    outcome_tail = Outcome("Tail")

    other_outcome_head = Outcome("Head")

    assert outcome_head != outcome_tail
    assert outcome_head == other_outcome_head


def test_discrete_outcome_equality():
    outcome_grade_10 = DiscreteOutcome("Grade", 10)
    outcome_grade_excellent = DiscreteOutcome("Grade", "Excellent")

    other_outcome_grade_excellent = DiscreteOutcome("Grade", "Excellent")

    assert outcome_grade_10 != outcome_grade_excellent
    assert outcome_grade_excellent == other_outcome_grade_excellent
