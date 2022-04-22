from functools import reduce
from typing import Any, Callable


class IPipeable:

  def pipe(self, *fns: Callable[[Any], Any]) -> Any:
    """

    Allows the use of function arguments consecutively

    Example:
        >>> pipe(x, fn) == __fn(x)  
        >>> pipe(x, fn, gn) == gn(fn(x))  
        ...
    """
    return reduce(lambda target, fn: fn(target), fns, self)