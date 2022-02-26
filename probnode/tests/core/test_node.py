from probnode import N, P, Event, SureEvent


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
  assert s.value == 0.8
  assert pd.value == 3