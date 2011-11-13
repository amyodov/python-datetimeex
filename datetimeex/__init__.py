#!/usr/bin/python
"""
The expanded versions of standard Python date/time-related classes,
capable for more operations.

Requires Python >= 2.6 (including Python 3.x).
"""

from _common import (MICROSECONDS_IN_SECOND, MICROSECONDS_IN_MINUTE,
                     MICROSECONDS_IN_HOUR, MICROSECONDS_IN_DAY,
                     t_to_mus, mus_to_t, td_to_mus, mus_to_td)
from _timeex import TimeEx
from _timedeltaex import TimeDeltaEx



# Run unittests, if executed directly.
if __name__ == "__main__":
    import doctest
    # Test this module
    doctest.testmod()
    # Test all the imported modules
    for modname in ("_common", "_timeex", "_timedeltaex"):
        mod = __import__(modname)
        doctest.testmod(mod)
