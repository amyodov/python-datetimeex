#!/usr/bin/python
# -*- coding: utf-8 -*-

import numbers, sys
from datetime import date, datetime, time, timedelta, tzinfo as tzinfo_class

MICROSECONDS_IN_SECOND = 1000000
MICROSECONDS_IN_MINUTE = MICROSECONDS_IN_SECOND * 60
MICROSECONDS_IN_HOUR = MICROSECONDS_IN_MINUTE * 60
MICROSECONDS_IN_DAY = MICROSECONDS_IN_HOUR * 24

_PY3K = (sys.version_info.major >= 3)


def t_to_mus(t):
    """
    Convert a datetime.time to microseconds elapsed since the midnight.

    Under Python 3.x, this function has two synonims:
    t_to_mus() and t_to_µs().

    >>> t_to_mus(time(3, 14, 15))
    11655000000
    >>> t_to_mus(time(3, 14, 15, 92))
    11655000092

    >>> # Test t_to_µs() in Python 3.x only
    >>> not _PY3K or eval("t_to_µs(time(3, 14, 15, 92)) == 11655000092")
    True
    """
    assert isinstance(t, time), repr(t)

    return (t.hour * MICROSECONDS_IN_HOUR +
            t.minute * MICROSECONDS_IN_MINUTE +
            t.second * MICROSECONDS_IN_SECOND +
            t.microsecond)

if _PY3K:
    exec("t_to_µs = t_to_mus")


def mus_to_t(microseconds, tzinfo=None):
    """
    Convert the number of microseconds elapsed since the midnight
    to datetime.time.
    If tzinfo argument is passed, it is written as is to the datetime.time.

    Sub-microsecond precision may be lost due to inherent storage limitations.
    Also, if the number of microseconds is higher than the number of microseconds
    in a typical Earth day, the modulo is taken automatically.

    Under Python 3.x, this function has two synonims:
    mus_to_t() and µs_to_t().

    >>> mus_to_t(11655000092)
    datetime.time(3, 14, 15, 92)

    >>> mus_to_t(11655000092.0002)
    datetime.time(3, 14, 15, 92)

    >>> mus_to_t(11655000092.0002, tzinfo=DummyTZInfo())
    datetime.time(3, 14, 15, 92, tzinfo=<DummyTZInfo>)

    >>> # Test µs_to_td() in Python 3.x only
    >>> not _PY3K or eval("µs_to_t(11655000092) == time(3, 14, 15, 92)")
    True
    """
    assert isinstance(microseconds, numbers.Number), repr(microseconds)
    assert tzinfo is None or isinstance(tzinfo, tzinfo_class), repr(tzinfo)

    s, _ms = divmod(int(microseconds), MICROSECONDS_IN_SECOND)
    m, _s = divmod(s, 60) # 60 seconds in a minute
    h, _m = divmod(m, 60) # 60 minutes in an hour
    _h = h % 24 # 24 hours in a day

    return time(hour = _h, minute = _m,
                second = _s, microsecond = _ms,
                tzinfo = tzinfo)

if _PY3K:
    exec("µs_to_t = mus_to_t")


def td_to_mus(td):
    """
    Convert a datetime.timedelta to microseconds.

    Under Python 3.x, this function has two synonims:
    td_to_mus() and td_to_µs().

    >>> td_to_mus(timedelta(3, 14, 15))
    259214000015

    >>> # Test td_to_µs() in Python 3.x only
    >>> not _PY3K or eval("td_to_µs(timedelta(3, 14, 15)) == 259214000015")
    True
    """
    assert isinstance(td, timedelta), repr(td)

    return (td.days * MICROSECONDS_IN_DAY +
            td.seconds * MICROSECONDS_IN_SECOND +
            td.microseconds)

if _PY3K:
    exec("td_to_µs = td_to_mus")


def mus_to_td(microseconds):
    """
    Convert an interval (in microseconds) to datetime.timedelta.

    Sub-microsecond precision may be lost due to inherent storage limitations.

    Under Python 3.x, this function has two synonims:
    mus_to_td() and µs_to_td().

    >>> mus_to_td(259214000015)
    datetime.timedelta(3, 14, 15)

    >>> mus_to_td(259214000015.0002)
    datetime.timedelta(3, 14, 15)

    >>> # Test µs_to_td() in Python 3.x only
    >>> not _PY3K or eval("µs_to_td(259214000015) == timedelta(3, 14, 15)")
    True
    """
    assert isinstance(microseconds, numbers.Number), repr(microseconds)

    return timedelta(microseconds = int(microseconds))

if _PY3K:
    exec("µs_to_td = mus_to_td")


class DummyTZInfo(tzinfo_class):
    def __repr__(self):
        return "<DummyTZInfo>"


# Run unittests, if executed directly.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
