from probnode import N, P, Event, SureEvent
from probnode.core.node_logic import additive_invert, reciprocate


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

  s1 = additive_invert(s)
  assert s1.value == 0 - s.value
  s2 = reciprocate(s)
  assert s2.value == 1 / s.value

  complex_s = s + pd
  assert complex_s.value == s.value + pd.value
  complex_s = s - pd
  assert complex_s.value == 0.6 - 0.2 - (0.6*0.2)