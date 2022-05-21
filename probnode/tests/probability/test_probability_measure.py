from probnode import p__X_, ES__, P__, Outcome, GenericSureEventSet
from pytest import raises


def test_probability_with_default_random_variable_measure_on_event_set():
  event_set = ES__(Outcome("sample"))
  p = p__X_(event_set)
  assert p.value == None


def test_probability_measure_with_random_variable_specified_on_event_set():
  humid_event_set = ES__(Outcome("humid"))
  rain_event_set = ES__(Outcome("rain"))

  def random_var(evt_set):
    if (evt_set == humid_event_set):
      return 0.4
    if (evt_set == rain_event_set):
      return 0.6
    return 0

  p_x = P__(random_var)

  p_humid = p_x(humid_event_set)
  p_rain = p_x(rain_event_set)

  assert p_humid.value == 0.4
  assert p_rain.value == 0.6
