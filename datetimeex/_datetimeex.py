#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numbers
from datetime import date, datetime, time, timedelta
from fractions import Fraction

from _common import (MICROSECONDS_IN_SECOND, MICROSECONDS_IN_MINUTE,
                     MICROSECONDS_IN_HOUR, MICROSECONDS_IN_DAY,
                     t_to_mus, mus_to_t, td_to_mus, mus_to_td,
                     _PY3K, DummyTZInfo)



class DateTimeEx(datetime):
    """
    Enhanced datetime.datetime, with various additional operations.
    """
    __slots__ = ()


    def __repr__(self):
        """
        >>> DateTimeEx(314, 1, 5)
        DateTimeEx(314, 1, 5, 0, 0)
        >>> DateTimeEx(314, 1, 5, tzinfo=DummyTZInfo())
        DateTimeEx(314, 1, 5, 0, 0, tzinfo=<DummyTZInfo>)

        >>> DateTimeEx(314, 1, 5, 9)
        DateTimeEx(314, 1, 5, 9, 0)
        >>> DateTimeEx(314, 1, 5, 9, tzinfo=DummyTZInfo())
        DateTimeEx(314, 1, 5, 9, 0, tzinfo=<DummyTZInfo>)

        >>> DateTimeEx(314, 1, 5, 9, 26)
        DateTimeEx(314, 1, 5, 9, 26)
        >>> DateTimeEx(314, 1, 5, 9, 26, tzinfo=DummyTZInfo())
        DateTimeEx(314, 1, 5, 9, 26, tzinfo=<DummyTZInfo>)

        >>> DateTimeEx(314, 1, 5, 9, 26, 53)
        DateTimeEx(314, 1, 5, 9, 26, 53)
        >>> DateTimeEx(314, 1, 5, 9, 26, 53, tzinfo=DummyTZInfo())
        DateTimeEx(314, 1, 5, 9, 26, 53, tzinfo=<DummyTZInfo>)

        >>> DateTimeEx(314, 1, 5, 9, 26, 53, 5897)
        DateTimeEx(314, 1, 5, 9, 26, 53, 5897)
        >>> DateTimeEx(314, 1, 5, 9, 26, 53, 5897, tzinfo=DummyTZInfo())
        DateTimeEx(314, 1, 5, 9, 26, 53, 5897, tzinfo=<DummyTZInfo>)
        """
        tzinfo = "" if self.tzinfo is None \
                    else ", tzinfo={0!r}".format(self.tzinfo)
        if not self.microsecond:
            if not self.second:
                return "DateTimeEx({0:d}, {1:d}, {2:d}, {3:d}, {4:d}{5:s})"\
                           .format(self.year, self.month, self.day,
                                   self.hour, self.minute,
                                   tzinfo)
            else:
                return "DateTimeEx({0:d}, {1:d}, {2:d}, {3:d}, {4:d}, {5:d}{6:s})"\
                           .format(self.year, self.month, self.day,
                                   self.hour, self.minute, self.second,
                                   tzinfo)
        else:
            return "DateTimeEx({0:d}, {1:d}, {2:d}, {3:d}, {4:d}, {5:d}, {6:d}{7:s})"\
                       .format(self.year, self.month, self.day,
                               self.hour, self.minute, self.second, self.microsecond,
                               tzinfo)


    def as_datetime(self):
        """
        Convert the DateTimeEx to the new datetime.datetime
        (even though DateTimeEx is its subclass and can be used instead
        almost anywhere).

        This is not a property, to reflect a fact that a new datetime.datetime
        is created rather than the access to the internals of DateTimeEx.

        >>> DateTimeEx(314, 1, 5, 9, 26, 53, 5897).as_datetime()
        datetime.datetime(314, 1, 5, 9, 26, 53, 5897)
        >>> DateTimeEx(314, 1, 5, 9, 26, 53, 5897, tzinfo=DummyTZInfo()).as_datetime()
        datetime.datetime(314, 1, 5, 9, 26, 53, 5897, tzinfo=<DummyTZInfo>)
        """
        return datetime(self.year, self.month, self.day,
                        self.hour, self.minute, self.second, self.microsecond,
                        self.tzinfo)

    @classmethod
    def from_datetime(cls, dt):
        """
        Create a new DateTimeEx from a basic datetime.datetime.

        >>> DateTimeEx.from_datetime(datetime(314, 1, 5, 9, 26, 53, 5897))
        DateTimeEx(314, 1, 5, 9, 26, 53, 5897)
        >>> DateTimeEx.from_datetime(datetime(314, 1, 5, 9, 26, 53, 5897, tzinfo=DummyTZInfo()))
        DateTimeEx(314, 1, 5, 9, 26, 53, 5897, tzinfo=<DummyTZInfo>)
        """
        return cls(dt.year, dt.month, dt.day,
                   dt.hour, dt.minute, dt.second, dt.microsecond,
                   dt.tzinfo)


'''
    @property
    def in_microseconds(self):
        """
        The number of microseconds elapsed Anno Domini.

        The number is always integer, due to the storage limitation.

        Under Python 3.x, this property has two synonims:
        in_microseconds and in_µs.

        >>> DateTimeEx(3, 14, 15, 92).in_microseconds
        11655000092

        >>> # Test µs_to_td() in Python 3.x only
        >>> not _PY3K or eval("DateTimeEx(3, 14, 15, 92).in_µs == 11655000092")
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
'''

# Run unittests, if executed directly.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
