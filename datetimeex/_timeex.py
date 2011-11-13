#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numbers
from datetime import date, datetime, time, timedelta, tzinfo as tzinfo_class
from fractions import Fraction

from _common import (MICROSECONDS_IN_SECOND, MICROSECONDS_IN_MINUTE,
                     MICROSECONDS_IN_HOUR, MICROSECONDS_IN_DAY,
                     t_to_mus, mus_to_t, td_to_mus, mus_to_td,
                     _PY3K, DummyTZInfo)



class TimeEx(time):
    """
    Enhanced datetime.time, with various additional operations.
    """
    __slots__ = ()


    def __repr__(self):
        """
        >>> TimeEx(0)
        TimeEx(0, 0)
        >>> TimeEx(0, tzinfo=DummyTZInfo())
        TimeEx(0, 0, tzinfo=<DummyTZInfo>)

        >>> TimeEx(3)
        TimeEx(3, 0)
        >>> TimeEx(3, tzinfo=DummyTZInfo())
        TimeEx(3, 0, tzinfo=<DummyTZInfo>)

        >>> TimeEx(3, 14)
        TimeEx(3, 14)
        >>> TimeEx(3, 14, tzinfo=DummyTZInfo())
        TimeEx(3, 14, tzinfo=<DummyTZInfo>)

        >>> TimeEx(3, 14, 15)
        TimeEx(3, 14, 15)
        >>> TimeEx(3, 14, 15, tzinfo=DummyTZInfo())
        TimeEx(3, 14, 15, tzinfo=<DummyTZInfo>)

        >>> TimeEx(3, 14, 15, 92)
        TimeEx(3, 14, 15, 92)
        >>> TimeEx(3, 14, 15, 92, tzinfo=DummyTZInfo())
        TimeEx(3, 14, 15, 92, tzinfo=<DummyTZInfo>)
        """
        tzinfo = "" if self.tzinfo is None \
                    else ", tzinfo={0!r}".format(self.tzinfo)
        if not self.microsecond:
            if not self.second:
                return "TimeEx({0:d}, {1:d}{2:s})"\
                           .format(self.hour, self.minute, tzinfo)
            else:
                return "TimeEx({0:d}, {1:d}, {2:d}{3:s})"\
                           .format(self.hour, self.minute, self.second, tzinfo)
        else:
            return "TimeEx({0:d}, {1:d}, {2:d}, {3:d}{4:s})"\
                       .format(self.hour, self.minute,
                               self.second, self.microsecond,
                               tzinfo)


    def as_time(self):
        """
        Convert the TimeEx to the new datetime.time
        (even though TimeEx is its subclass and can be used instead
        almost anywhere).

        This is not a property, to reflect a fact that a new datetime.time
        is created rather than the access to the internals of TimeEx.

        >>> TimeEx(3, 14, 15, 92).as_time()
        datetime.time(3, 14, 15, 92)

        >>> TimeEx(3, 14, 15, 92, DummyTZInfo()).as_time()
        datetime.time(3, 14, 15, 92, tzinfo=<DummyTZInfo>)
        """
        return time(self.hour, self.minute,
                    self.second, self.microsecond,
                    self.tzinfo)


    @classmethod
    def from_time(cls, t):
        """
        Create a new TimeEx from a basic datetime.time.

        >>> TimeEx.from_time(time(3, 14, 15, 92))
        TimeEx(3, 14, 15, 92)

        >>> TimeEx.from_time(time(3, 14, 15, 92, DummyTZInfo()))
        TimeEx(3, 14, 15, 92, tzinfo=<DummyTZInfo>)
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
    def from_microseconds(cls, microseconds, tzinfo=None):
        """
        Given the number of microseconds elapsed since the midnight,
        create the appropriate TimeEx object. If tzinfo argument is passed,
        it is written as is to the TimeEx.

        Sub-microsecond precision may be lost due to inherent storage limitations.
        Also, if the number of microseconds is higher than the number of microseconds
        in a typical Earth day, the modulo is taken automatically.

        Under Python 3.x, this function has two synonims:
        from_microseconds() and from_µs().

        >>> TimeEx.from_microseconds(11655000092)
        TimeEx(3, 14, 15, 92)
        >>> TimeEx.from_microseconds(11655000092.003)
        TimeEx(3, 14, 15, 92)
        >>> TimeEx.from_microseconds(11655000092.003, tzinfo=DummyTZInfo())
        TimeEx(3, 14, 15, 92, tzinfo=<DummyTZInfo>)

        # Test from_µs() in Python 3.x only
        >>> not _PY3K or eval("TimeEx.from_µs(11655000092) == \
            TimeEx(3, 14, 15, 92)")
        True

        @type microseconds: numbers.Number
        @type tzinfo: NoneType, tzinfo

        @rtype: TimeEx
        """
        assert isinstance(microseconds, numbers.Number), repr(microseconds)
        assert tzinfo is None or isinstance(tzinfo, tzinfo_class), repr(tzinfo)

        return cls.from_time(mus_to_t(microseconds, tzinfo=tzinfo))

    if _PY3K:
        exec("from_µs = from_microseconds")


    def __add__(self, summand):
        """
        Add this TimeEx to a datetime.timedelta
        (with possible wrapping at the midnight).

        >>> TimeEx(23, 44, 55) + timedelta(hours=3, minutes=20)
        TimeEx(3, 4, 55)
        >>> TimeEx(23, 44, 55, tzinfo=DummyTZInfo()) + \
            timedelta(hours=3, minutes=20)
        TimeEx(3, 4, 55, tzinfo=<DummyTZInfo>)

        @type summand: timedelta
        @rtype: TimeEx
        """
        if isinstance(summand, timedelta):
            return TimeEx.from_microseconds(self.in_microseconds + td_to_mus(summand),
                                            tzinfo=self.tzinfo)
        else:
            raise NotImplementedError("{0!r} + {1!r}".format(self, summand))

    __radd__ = __add__


    def __sub__(self, subtrahend):
        """
        Subtract a datetime.time or datetime.timedelta
        (with possible wrapping at the midnight)
        from the TimeEx.

        Whenever the subtrahend is the datetime.time,
        the result is a TimeDeltaEx.

        Whenever the subtrahend is the datetime.timedelta,
        the result is a TimeEx.

        >>> TimeEx(3, 4, 15, 92) - timedelta(0, 2, 71, 82)
        TimeEx(3, 4, 12, 918021)
        >>> TimeEx(3, 4, 15, 92) - timedelta(2, 71, 82, 81)
        TimeEx(3, 3, 3, 919010)
        >>> TimeEx(3, 4, 15, 92, tzinfo=DummyTZInfo()) - timedelta(2, 71, 82, 81)
        TimeEx(3, 3, 3, 919010, tzinfo=<DummyTZInfo>)

        @type subtrahend: time, timedelta
        @rtype: TimeEx, TimeDeltaEx
        """
        # TODO: HOW TO SUBTRACT DATETIME.TIME, ESPECIALLY TZ-AWARE?
        if isinstance(subtrahend, timedelta):
            return TimeEx.from_microseconds(self.in_microseconds - td_to_mus(subtrahend),
                                            tzinfo=self.tzinfo)
        else:
            raise NotImplementedError("{0!r} - {1!r}".format(self, subtrahend))


#    def __rsub__(self, td):
#        """
#        Subtract a datetime.timedelta from the TimeEx
#        (with possible wrapping at the midnight).
#
#        >>> TimeEx(3, 4, 55) - timedelta(hours = 3, minutes = 20)
#        TimeEx(23, 44, 55)
#
#        @type summand: timedelta
#        @rtype: TimeEx
#        """
#        assert isinstance(td, timedelta), repr(td)
#
#        return TimeEx.from_microseconds(self.in_microseconds - td_to_mus(other))


# Run unittests, if executed directly.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
