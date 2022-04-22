from functools import reduce
from typing import Any, Callable


class IReducible:

  def reduce(self, *fns: Callable[[Any], Any]) -> Any:
    """

    Allows the use of function arguments consecutively

    Example:
        >>> reduce(x, fn) == __fn(x)  
        >>> reduce(x, fn, gn) == gn(fn(x))  
        ...
    """
    return reduce(lambda target, fn: fn(target), fns, self)