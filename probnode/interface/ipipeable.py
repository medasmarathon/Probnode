from functools import reduce
from typing import Any, Callable


class IPipeable:

  def pipe(self, *fns: Callable[[Any], Any]) -> Any:
    """

    Allows the use of function arguments consecutively

    Example:
        >>> x.pipe(fn) == __fn(x)  
        >>> x.pipe(fn, gn) == gn(fn(x))  
        ...
    """
    return reduce(lambda target, fn: fn(target), fns, self)