from probnode import N, P, Event, SureEvent
from pytest import raises


def test_node_value_from_probability():
  p = P(Event("sample"))
  n = N(p)
  assert n.value == None

  p.value = 0.6
  assert n.value == 0.6


def test_chain_node_value():
  p1 = P(Event("sample1"))
  n1 = N(p1)
  p2 = P(Event("sample2"))
  n2 = N(p2)
  s = n1 + n2
  pd = n1 / n2
  assert s.value == None
  assert pd.value == None

  p1.value = 0.6
  p2.value = 0.2
  assert s.value == 0.6 + 0.2
  assert pd.value == 3

  s = n1 - n2
  assert s.value == 0.6 - 0.2
  pd = n1 * n2
  assert pd.value == 0.6 * 0.2

  s1 = s.additive_invert()
  assert s1.value == 0 - s.value
  s2 = s.reciprocate()
  assert s2.value == 1 / s.value

  complex_s = s + pd
  assert complex_s.value == s.value + pd.value
  complex_s = s - pd
  assert complex_s.value == 0.6 - 0.2 - (0.6*0.2)


def test_node_value_from_prob_distribution_function():
  p1 = P(Event("sample1"))
  n1 = N(p1)
  p2 = P(Event("sample2"))
  n2 = N(p2)
  p1.value = lambda x: x * 2
  assert p1.value(2) == 4

  with raises(TypeError):
    p1.value == 0
