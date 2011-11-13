#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numbers
from datetime import date, datetime, time, timedelta
from fractions import Fraction

from _common import (MICROSECONDS_IN_SECOND, MICROSECONDS_IN_MINUTE,
                     MICROSECONDS_IN_HOUR, MICROSECONDS_IN_DAY,
                     td_to_mus, mus_to_td,
                     _PY3K)
from _timeex import TimeEx


class TimeDeltaEx(timedelta, numbers.Real):
    """
    Enhanced datetime.TimeDelta, with various additional operations.
    """
    __slots__ = ()


    def __repr__(self):
        """
        >>> TimeDeltaEx.from_timedelta(timedelta(0))
        TimeDeltaEx(0)
        >>> TimeDeltaEx.from_timedelta(timedelta(3))
        TimeDeltaEx(3)
        >>> TimeDeltaEx.from_timedelta(timedelta(3, 14))
        TimeDeltaEx(3, 14)
        >>> TimeDeltaEx.from_timedelta(timedelta(3, 14, 15))
        TimeDeltaEx(3, 14, 15)
        """
        if not self.microseconds:
            if not self.seconds:
                return "TimeDeltaEx({0:d})".format(self.days)
            else:
                return "TimeDeltaEx({0:d}, {1:d})".format(self.days, self.seconds)
        else:
            return "TimeDeltaEx({0:d}, {1:d}, {2:d})"\
                       .format(self.days, self.seconds, self.microseconds)


    def as_timedelta(self):
        """
        Convert the TimeDeltaEx to the new datetime.timedelta
        (even though TimeDeltaEx is its subclass and can be used instead
        almost anywhere).

        This is not a property, to reflect a fact that a new datetime.timedelta
        is created rather than the access to the internals of TimeDeltaEx.

        >>> TimeDeltaEx(3, 14, 15).as_timedelta()
        datetime.timedelta(3, 14, 15)

        @rtype: timedelta
        """
        return timedelta(self.days, self.seconds, self.microseconds)


    @classmethod
    def from_timedelta(cls, td):
        """
        Create a new TimeDeltaEx from a basic datetime.timedelta.

        >>> TimeDeltaEx.from_timedelta(timedelta(3, 14, 15))
        TimeDeltaEx(3, 14, 15)

        @type td: timedelta
        @rtype: TimeDeltaEx
        """
        assert isinstance(td, timedelta), repr(td)

        return cls(td.days, td.seconds, td.microseconds)


    @property
    def in_microseconds(self):
        """
        The number of microseconds in the time interval.

        The number is always integer, due to inherent storage limitation.

        Under Python 3.x, this property has two synonims:
        in_microseconds and in_µs.

        >>> TimeDeltaEx(3, 14, 15).in_microseconds
        259214000015

        >>> # Test µs_to_td() in Python 3.x only
        >>> not _PY3K or eval("TimeDeltaEx(3, 14, 15).in_microseconds == 259214000015")
        True

        @rtype: numbers.Number
        """
        return td_to_mus(self)

    if _PY3K:
        exec("in_µs = in_microseconds")


    @classmethod
    def from_microseconds(cls, microseconds):
        """
        Given a (numeric) duration in microseconds, create
        the appropriate TimeDeltaEx.

        Sub-microsecond precision may be lost due to inherent storage limitations.

        Under Python 3.x, this function has two synonims:
        from_microseconds() and from_µs().

        >>> TimeDeltaEx.from_microseconds(259214000015)
        TimeDeltaEx(3, 14, 15)

        >>> TimeDeltaEx.from_microseconds(259214000015.222)
        TimeDeltaEx(3, 14, 15)

        # Test from_µs() in Python 3.x only
        >>> not _PY3K or eval("TimeDeltaEx.from_µs(259214000015) == \
            TimeDeltaEx(3, 14, 15)")
        True

        @type microseconds: numbers.Number
        @rtype: TimeDeltaEx
        """
        assert isinstance(microseconds, numbers.Number), repr(microseconds)

        return cls(microseconds = microseconds)

    if _PY3K:
        exec("from_µs = from_microseconds")


    @property
    def in_seconds(self):
        """
        The number of seconds in the time interval.

        As the object may have sub-second precision, to represent
        as the number of seconds this property provides a fractions.Fraction.

        >>> TimeDeltaEx(3, 14, 15).in_seconds
        Fraction(51842800003, 200000)

        >>> str(TimeDeltaEx(3, 14, 15).in_seconds)
        '51842800003/200000'

        >>> float(TimeDeltaEx(3, 14, 15).in_seconds)
        259214.000015

        @rtype: numbers.Rational
        """
        return Fraction(self.in_microseconds, 1000000)


    def __div__(self, divisor):
        """
        Divide TimeDeltaEx by some datetime.timedelta or a number.

        For dividing TimeDeltaEx by datetime.timedelta,
        the result will be a ratio.
        For dividing TimeDeltaEx by a number, the result will be a TimeDeltaEx
        (the precision may be lost though).

        >>> TimeDeltaEx(seconds = 5) / timedelta(seconds = 2)
        Fraction(5, 2)

        >>> TimeDeltaEx(seconds = 5) / 4
        TimeDeltaEx(0, 1, 250000)

        >>> TimeDeltaEx(microseconds = 75) / 2.5
        TimeDeltaEx(0, 0, 30)

        @type divisor: timedelta, numbers.Number
        @rtype: TimeDeltaEx, numbers.Rational
        """
        if isinstance(divisor, timedelta):
            return Fraction(self.in_microseconds, td_to_mus(divisor))
        elif isinstance(divisor, numbers.Number):
            return TimeDeltaEx.from_microseconds(self.in_microseconds / divisor)
        else:
            raise NotImplementedError("{0!r} / {1!r}".format(self, divisor))

    __truediv__ = __div__


    def __rdiv__(self, dividend):
        """
        The dividend is divided by this TimeDeltaEx.

        The dividend must be a datetime.timedelta.
        The result is a ratio.

        >>> timedelta(seconds = 5) / TimeDeltaEx(seconds = 2)
        Fraction(5, 2)

        @type dividend: timedelta
        @rtype: numbers.Rational
        """
        assert isinstance(dividend, (timedelta, numbers.Number)), \
               repr(dividend)

        return Fraction(td_to_mus(dividend), self.in_microseconds)

    __rtruediv__ = __rdiv__


    def __floordiv__(self, divisor):
        """
        Divide TimeDeltaEx by some datetime.timedelta or a number,
        with subsequent flooring to the integer value.

        For dividing TimeDeltaEx by datetime.timedelta,
        the result will be an integer number.
        For dividing TimeDeltaEx by a number, the result will be a TimeDeltaEx
        (the precision may be lost though).

        >>> TimeDeltaEx(seconds = 5) // timedelta(seconds = 2)
        2
        >>> TimeDeltaEx(seconds = 5) // 4
        TimeDeltaEx(0, 1, 250000)
        >>> TimeDeltaEx(microseconds = 75) // 2.6
        TimeDeltaEx(0, 0, 28)

        @type divisor: timedelta, numbers.Number
        @rtype: TimeDeltaEx, numbers.Number
        """
        if isinstance(divisor, timedelta):
            return self.in_microseconds // td_to_mus(divisor)
        elif isinstance(divisor, numbers.Number):
            return TimeDeltaEx.from_microseconds(self.in_microseconds //
                                                 divisor)
        else:
            raise NotImplementedError("{0!r} // {1!r}!".format(self, divisor))


    def __rfloordiv__(self, dividend):
        """
        The dividend is divided by this TimeDeltaEx,
        with subsequent flooring to the integer value.

        The dividend must be a datetime.timedelta (or any compatible subclass).
        The result is a number.

        >>> timedelta(seconds = 5) // TimeDeltaEx(seconds = 2)
        2

        @type dividend: timedelta
        @rtype: number.Number
        """
        assert isinstance(dividend, timedelta), repr(dividend)

        return td_to_mus(dividend) // self.in_microseconds


    def __mod__(self, divisor):
        """
        Find modulo for division of TimeDeltaEx by some
        datetime.timedelta.

        For dividing TimeDeltaEx by a datetime.timedelta,
        the modulo will be a TimeDeltaEx.
        The modulo for dividing TimeDeltaEx by a regular number
        is not defined.

        >>> TimeDeltaEx(seconds = 42) % timedelta(seconds = 11)
        TimeDeltaEx(0, 9)

        @type divisor: timedelta
        @rtype: TimeDeltaEx
        """
        if isinstance(divisor, timedelta):
            return TimeDeltaEx.from_microseconds(self.in_microseconds %
                                                 td_to_mus(divisor))
        else:
            raise NotImplementedError("{0!r} % {1!r}".format(self, divisor))


    def __rmod__(self, dividend):
        """
        Find modulo for division of some datetime.timedelta
        by the TimeDeltaEx.

        For dividing some datetime.timedelta by this TimeDeltaEx,
        the modulo will be a TimeDeltaEx.
        The modulo for dividing any other type by this TimeDeltaEx
        is not defined.

        >>> timedelta(seconds = 42) % TimeDeltaEx(seconds = 11)
        TimeDeltaEx(0, 9)

        @type dividend: timedelta
        @rtype: TimeDeltaEx
        """
        assert isinstance(dividend, timedelta), repr(dividend)

        return TimeDeltaEx.from_microseconds(td_to_mus(dividend) %
                                             self.in_microseconds)


    def __divmod__(self, divisor):
        """
        Calculate both the result of division and the modulo
        for division of this TimeDeltaEx by some datetime.timedelta.

        Even though the TimeDeltaEx may be divided to the regular number,
        the modulo for such operation cannot be calculated.

        >>> divmod(TimeDeltaEx(seconds = 42), timedelta(seconds = 11))
        (3, TimeDeltaEx(0, 9))

        @type divisor: timedelta
        @rtype: tuple
        """
        if isinstance(divisor, timedelta):
            _d, _m = divmod(self.in_microseconds, td_to_mus(divisor))
            return (_d, TimeDeltaEx.from_microseconds(_m))
        else:
            raise NotImplementedError("divmod({0!r}, {1!r})"
                                          .format(self, divisor))


    def __rdivmod__(self, dividend):
        """
        Calculate both the result of division and the modulo
        for division of some datetime.timedelta by this TimeDeltaEx.

        >>> divmod(timedelta(seconds = 42), TimeDeltaEx(seconds = 11))
        (3, TimeDeltaEx(0, 9))

        @type dividend: timedelta
        @rtype: TimeDeltaEx
        """
        assert isinstance(dividend, timedelta), repr(dividend)

        _d, _m = divmod(td_to_mus(dividend), self.in_microseconds)
        return (_d, TimeDeltaEx.from_microseconds(_m))


    def __mul__(self, n):
        """
        Multiplicate the TimeDeltaEx by a number.

        The sub-microsecond precision may be lost.

        >>> TimeDeltaEx(seconds = 5) * 5
        TimeDeltaEx(0, 25)
        >>> 5 * TimeDeltaEx(seconds = 5)
        TimeDeltaEx(0, 25)
        >>> TimeDeltaEx(microseconds = 50) * 0.77
        TimeDeltaEx(0, 0, 39)
        >>> 0.77 * TimeDeltaEx(microseconds = 50)
        TimeDeltaEx(0, 0, 39)

        @type other: numbers.Number
        @rtype: TimeDeltaEx
        """
        if isinstance(n, numbers.Number):
            return TimeDeltaEx.from_microseconds(self.in_microseconds * n)
        else:
            raise NotImplementedError("{0!r} * {1!r}".format(self, n))

    __rmul__ = __mul__


    def __add__(self, summand):
        """
        Add this TimeDeltaEx to the datetime.date, datetime.datetime,
        datetime.time (with possible wrapping at the midnight),
        or to the datetime.timedelta.

        Whenever another summand is the datetime.date,
        the result is automatically enhanced from datetime.date to DateEx.

        Whenever another summand is the datetime.datetime,
        the result is automatically enhanced from datetime.datetime to DateTimeEx.

        Whenever another summand is the datetime.time,
        the result is automatically enhanced from datetime.time to TimeEx.

        Whenever another summand is the datetime.timedelta,
        the result is automatically enhanced from datetime.timedelta
        to TimeDeltaEx.

        >>> time(23, 44, 55) + TimeDeltaEx(hours = 3, minutes = 20)
        TimeEx(3, 4, 55)
        >>> TimeEx(23, 44, 55) + TimeDeltaEx(hours = 3, minutes = 20)
        TimeEx(3, 4, 55)

        >>> TimeDeltaEx(hours = 3, minutes = 20) + time(23, 44, 55)
        TimeEx(3, 4, 55)
        >>> TimeDeltaEx(hours = 3, minutes = 20) + TimeEx(23, 44, 55)
        TimeEx(3, 4, 55)

        >>> TimeDeltaEx(3, 14, 15, 92) + timedelta(2, 71, 82, 81)
        TimeDeltaEx(5, 85, 173097)
        >>> timedelta(2, 71, 82, 81) + TimeDeltaEx(3, 14, 15, 92)
        TimeDeltaEx(5, 85, 173097)
        """
        assert isinstance(summand, (date, datetime, time, timedelta)), \
               repr(td)

        if isinstance(summand, date):
            # TODO
            raise NotImplementedError("Not yet implemented!")
        elif isinstance(summand, datetime):
            # TODO
            raise NotImplementedError("Not yet implemented!")
        elif isinstance(summand, time):
            if isinstance(summand, TimeEx):
                # Shortcut
                return TimeEx.from_microseconds(self.in_microseconds +
                                                summand.in_microseconds)
            else:
                return TimeEx.from_microseconds(self.in_microseconds +
                                                TimeEx.from_time(summand).in_microseconds)
        elif isinstance(summand, timedelta):
            return TimeDeltaEx.from_microseconds(td_to_mus(self) + td_to_mus(summand))
        else:
            raise NotImplementedError("{0!r} + {1!r}".format(self, summand))

    __radd__ = __add__


    def __sub__(self, subtrahend):
        """
        Subtract a datetime.timedelta from this TimeDeltaEx.

        >>> TimeDeltaEx(3, 4, 15, 92) - timedelta(2, 71, 82, 81)
        TimeDeltaEx(0, 86333, 10933)
        >>> TimeDeltaEx(2, 71, 82, 81) - timedelta(3, 4, 15, 92)
        TimeDeltaEx(-1, 66, 989067)
        """
        if isinstance(subtrahend, timedelta):
            return TimeDeltaEx.from_microseconds(self.in_microseconds -
                                                 td_to_mus(subtrahend))
        else:
            raise NotImplementedError("{0!r} - {1!r}".format(self, subtrahend))


    def __rsub__(self, minuend):
        """
        This TimeDeltaEx is subtracted from the datetime.date, datetime.datetime,
        datetime.time (with possible wrapping at the midnight),
        or  datetime.timedelta.

        Whenever the minuend is the datetime.date,
        the result is automatically enhanced from datetime.date to DateEx.

        Whenever the minuend is the datetime.datetime,
        the result is automatically enhanced from datetime.datetime to DateTimeEx.

        Whenever the minuend is the datetime.time,
        the result is automatically enhanced from datetime.time to TimeEx.

        Whenever the minuend is the datetime.timedelta,
        the result is automatically enhanced from datetime.timedelta
        to TimeDeltaEx.

        >>> TimeEx(3, 4, 15, 92) - TimeDeltaEx(0, 2, 71, 82)
        TimeEx(3, 4, 12, 918021)
        >>> TimeEx(3, 4, 15, 92) - TimeDeltaEx(2, 71, 82, 81)
        TimeEx(3, 3, 3, 919010)

        >>> time(3, 4, 15, 92) - TimeDeltaEx(0, 2, 71, 82)
        TimeEx(3, 4, 12, 918021)
        >>> time(3, 4, 15, 92) - TimeDeltaEx(2, 71, 82, 81)
        TimeEx(3, 3, 3, 919010)

        >>> timedelta(3, 4, 15, 92) - TimeDeltaEx(2, 71, 82, 81)
        TimeDeltaEx(0, 86333, 10933)
        >>> timedelta(2, 71, 82, 81) - TimeDeltaEx(3, 4, 15, 92)
        TimeDeltaEx(-1, 66, 989067)
        """
        if isinstance(minuend, time):
            if isinstance(minuend, TimeEx):
                # Shortcut
                return TimeEx.from_microseconds(minuend.in_microseconds -
                                                self.in_microseconds)
            else:
                return TimeEx.from_microseconds(TimeEx.from_time(minuend).in_microseconds -
                                                self.in_microseconds)
        elif isinstance(minuend, timedelta):
            return TimeDeltaEx.from_microseconds(td_to_mus(minuend) -
                                                 self.in_microseconds)
        elif isinstance(minuend, date):
            # TODO
            raise NotImplementedError("Not yet implemented!")
        elif isinstance(minuend, datetime):
            # TODO
            raise NotImplementedError("Not yet implemented!")
        else:
            raise NotImplementedError("{0!r} - {1!r}".format(minuend, self))



# Run unittests, if executed directly.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
