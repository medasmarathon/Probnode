from dataclasses import dataclass, field
from probnode.interface.iexperiment import IExperiment, ITrial, ITrialResult
from probnode.interface.isample_space import ISampleSpace


@dataclass(frozen=True, eq=True)
class Experiment(IExperiment):
  name: str = field()
  sample_space: ISampleSpace = field(default=None)

@dataclass(frozen=True, eq=True)
class Trial(ITrial):
  name: str = field()

@dataclass(frozen=True, eq=True)
class TrialResult(ITrialResult):
  name: str = field()
  trial: ITrial = field(default=None)
