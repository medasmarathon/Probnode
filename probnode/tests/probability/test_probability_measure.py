from probnode import p__X, ES, Outcome, GenericSureEventSet
from pytest import raises


def test_probability_measure_from_event_set():
  event_set = ES(Outcome("sample"))
  p = p__X(event_set)
  assert p.value == None

  event_set.value = 0.6
  assert p.value == 0.6


def test_chain_prob_measure_value():
  event_set_1 = ES(Outcome("sample1"))
  p1 = p__X(event_set_1)
  event_set_2 = ES(Outcome("sample2"))
  p2 = p__X(event_set_2)
  s = p1 + p2
  pd = p1 / p2
  assert s.value == None
  assert pd.value == None

  event_set_1.value = 0.6
  event_set_2.value = 0.2
  assert s.value == 0.6 + 0.2
  assert pd.value == 3

  s = p1 - p2
  assert s.value == 0.6 - 0.2
  pd = p1 * p2
  assert pd.value == 0.6 * 0.2

  s1 = s.additive_invert()
  assert s1.value == 0 - s.value
  s2 = s.reciprocate()
  assert s2.value == 1 / s.value

  complex_s = s + pd
  assert complex_s.value == s.value + pd.value
  complex_s = s - pd
  assert complex_s.value == 0.6 - 0.2 - (0.6*0.2)
