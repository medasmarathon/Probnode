from probnode import ProbabilityMeasure, Event, P__, Outcome, GenericSureEvent
from pytest import raises
from probnode import RandomVariable
from probnode.datatype.probability_function import ProbabilityFunction


def test_probability_with_default_random_variable_measure_on_event_set():
  event = Event(Outcome("sample"))
  p = ProbabilityMeasure(event)
  assert p.value == None


def test_probability_measure_with_random_variable_specified_on_event_set():
  humid_event = Event(Outcome("humid"))
  rain_event = Event(Outcome("rain"))

  def prob_logic_func(evt_set):
    if (evt_set == humid_event):
      return 0.4
    if (evt_set == rain_event):
      return 0.6
    return 0

  p_x = P__(RandomVariable(ProbabilityFunction(prob_logic_func)))

  p_humid = p_x(humid_event)
  p_rain = p_x(rain_event)

  assert p_humid.value == 0.4
  assert p_rain.value == 0.6
