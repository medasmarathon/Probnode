from probnode import ProbabilityMeasureOfEvent, Event, P__, Outcome, GenericSureEvent
from pytest import raises
from probnode import RandomVariable
from probnode import ProbabilityDistribution
from probnode.computation import eval


def test_probability_with_default_random_variable_measure_on_event_set():
  event = Event(Outcome("sample"))
  p = ProbabilityMeasureOfEvent(event)
  assert eval(p) == None


def test_probability_measure_with_random_variable_specified_on_event_set():
  humid_event = Event(Outcome("humid"))
  rain_event = Event(Outcome("rain"))

  def prob_logic_func(evt_set):
    if (evt_set == humid_event):
      return 0.4
    if (evt_set == rain_event):
      return 0.6
    return 0

  p_x = P__(RandomVariable(ProbabilityDistribution(prob_logic_func)))

  p_humid = p_x(humid_event)
  p_rain = p_x(rain_event)

  assert eval(p_humid) == 0.4
  assert eval(p_rain) == 0.6


def test_complex_p_measure_with_random_variable_specified_on_event_set():
  humid_event = Event(Outcome("humid"))
  rain_event = Event(Outcome("rain"))
  sunny_event = Event(Outcome("sunny"))

  def prob_logic_func(evt_set):
    if (evt_set == humid_event):
      return 0.1
    if (evt_set == rain_event):
      return 0.2
    if (evt_set == sunny_event):
      return 0.4
    return 0

  p_x = P__(RandomVariable(ProbabilityDistribution(prob_logic_func)))

  p_humid = p_x(humid_event)
  p_rain = p_x(rain_event)
  p_sun = p_x(sunny_event)

  assert eval(p_humid + p_rain) == 0.1 + 0.2
  assert eval(p_rain - p_humid) == 0.2 - 0.1
  assert eval(p_rain - p_humid*p_sun) == 0.2 - 0.1*0.4
  assert eval(p_rain/p_humid - p_sun) == 0.2/0.1 - 0.4
