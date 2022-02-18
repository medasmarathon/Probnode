from typing import List, Tuple
import pytest
from probnode import *
from probnode.probability.probability import *
from probnode.computation.contract import *


def test_remove_same_exp_in_simple_vs_and_prob_lists():
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_x_and_y = P(prob_x & prob_y)
  assert remove_same_exp_in_simple_vs_and_prob_lists([prob_x],
                                                     [prob_x_and_y]) == ([prob_x], [prob_x_and_y])
