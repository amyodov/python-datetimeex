#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numbers
from datetime import date, datetime, time, timedelta
from fractions import Fraction

from _common import (MICROSECONDS_IN_SECOND, MICROSECONDS_IN_MINUTE,
                     MICROSECONDS_IN_HOUR, MICROSECONDS_IN_DAY,
                     t_to_mus, mus_to_t, td_to_mus, mus_to_td,
                     _PY3K)



class TimeEx(time):
    """
    Enhanced datetime.Time, with various additional operations.
    """
    __slots__ = ()


    def __repr__(self):
        """
        >>> TimeEx(0)
        TimeEx(0)
        >>> TimeEx(3)
        TimeEx(3)
        >>> TimeEx(3, 14)
        TimeEx(3, 14)
        >>> TimeEx(3, 14, 15)
        TimeEx(3, 14, 15)
        >>> TimeEx(3, 14, 15, 92)
        TimeEx(3, 14, 15, 92)
        """
        if not self.microsecond:
            if not self.second:
                if not self.minute:
                    return "TimeEx({0:d})".format(self.hour)
                else:
                    return "TimeEx({0:d}, {1:d})".format(self.hour, self.minute)
            else:
                return "TimeEx({0:d}, {1:d}, {2:d})"\
                           .format(self.hour, self.minute, self.second)
        else:
            return "TimeEx({0:d}, {1:d}, {2:d}, {3:d})"\
                       .format(self.hour, self.minute,
                               self.second, self.microsecond)


    FORMAT_STRING = "%H:%M:%S.%f"

    def as_time(self):
        """
        Convert the TimeEx to the new datetime.time
        (even though TimeEx is its subclass and can be used instead
        almost anywhere).

        This is not a property, to reflect a fact that a new datetime.time
        is created rather than the access to the internals of TimeEx.

        >>> TimeEx(3, 14, 15, 92).as_time()
        datetime.time(3, 14, 15, 92)
        """
        return time(self.hour, self.minute, self.second, self.microsecond)


    @classmethod
    def from_time(cls, t):
        """
        Create a new TimeEx from a basic datetime.time.

        >>> TimeEx.from_time(time(3, 14, 15, 92))
        TimeEx(3, 14, 15, 92)
        """
        return cls(t.hour, t.minute, t.second, t.microsecond, t.tzinfo)


    @property
    def in_microseconds(self):
        """
        The number of microseconds elapsed since the midnight.

        The number is always integer, due to the storage limitation.

        Under Python 3.x, this property has two synonims:
        in_microseconds and in_µs.

        >>> TimeEx(3, 14, 15, 92).in_microseconds
        11655000092

        >>> # Test µs_to_td() in Python 3.x only
        >>> not _PY3K or eval("TimeEx(3, 14, 15, 92).in_µs == 11655000092")
        True

        @rtype: numbers.Number
        """
        return t_to_mus(self)

    if _PY3K:
        exec("in_µs = in_microseconds")


    @classmethod
    def from_microseconds(cls, microseconds):
        """
        Given the number of microseconds elapsed since the midnight,
        create the appropriate TimeEx object.

        Sub-microsecond precision may be lost due to inherent storage limitations.
        Also, if the number of microseconds is higher than the number of microseconds
        in a typical Earth day, the modulo is taken automatically.

        Under Python 3.x, this function has two synonims:
        from_microseconds() and from_µs().

        >>> TimeEx.from_microseconds(11655000092)
        TimeEx(3, 14, 15, 92)
        >>> TimeEx.from_microseconds(11655000092.003)
        TimeEx(3, 14, 15, 92)

        # Test from_µs() in Python 3.x only
        >>> not _PY3K or eval("TimeEx.from_µs(11655000092) == \
            TimeEx(3, 14, 15, 92)")
        True

        @type microseconds: numbers.Number

        @rtype: TimeEx
        """
        assert isinstance(microseconds, numbers.Number), repr(microseconds)

        return cls.from_time(mus_to_t(microseconds))

    if _PY3K:
        exec("from_µs = from_microseconds")


##    def __add__(self, td):
#        """
#        Add a datetime.timedelta to the TimeEx
#        (with possible wrapping at the midnight).
#
#        >>> TimeEx(23, 44, 55) + timedelta(hours = 3, minutes = 20)
#        TimeEx(3, 4, 55)
#        """
#        assert isinstance(td, timedelta), repr(td)
#
#        return TimeEx.from_microseconds(self.in_microseconds + td_to_mus(td))


#    def __sub__(self, td):
#        """
#        Subtract a datetime.timedelta from the TimeEx
#        (with possible wrapping at the midnight).
#
#        >>> TimeEx(3, 4, 55) - timedelta(hours = 3, minutes = 20)
#        TimeEx(23, 44, 55)
#        """
#        assert isinstance(td, timedelta), repr(td)
#
#        return TimeEx.from_microseconds(self.in_microseconds - td_to_mus(other))


# Run unittests, if executed directly.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
