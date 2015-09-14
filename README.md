# Summary

This project provides the expanded versions of standard Python date/time-related classes, capable for more operations (e.g. divide timedelta by timedelta).

# Usage

If you ever considered the standard `ddatetime.timedelta`, `datetime.datetime` and similar object very limited in capabilities – e.g. if you ever tried to add a `datetime.timedelta` to `datetime.time` (assuming the time will be wrapped at the midnight boundary) and found out you cannot do that, or if you ever tried to calculate what time interval is precisely twice shorter than “3 days, 5 hours and 53 minutes” – now you have a tool for that. ```

    >>> from datetimeex import TimeEx, TimeDeltaEx
    >>> str(TimeEx(hour = 23, minute = 41) + TimeDeltaEx(minutes = 45)) 
    '00:26:00' 
    >>> str(TimeDeltaEx(days = 3, hours = 5, minutes = 53) / 2) 
    '1 day, 14:56:30'

There are also easy ways to convert existing `datetime.timedelta`/`datetime.datetime`/etc objects to their `'…Ex'` counterparts, including the fact that almost any binary operation involving an `…Ex` object results in an `…Ex` object:

    >>> from datetime import time 
    >>> from datetimeex import TimeDeltaEx 
    >>> time(hour = 5) + TimeDeltaEx(minutes = 7) 
    TimeEx(5, 7)

# Disclaimer

This code is in a very early state, and not all expected operations are yet supported. Though the operations which are supported are working good enough.

Feel free to send me comments and pull requests.
