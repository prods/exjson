from datetime import datetime

from dateutil.tz import tzlocal

_DATETIME_FORMAT_MAP = [
    (0, "dddd", "%A"),  # Weekday as locale’s full name. Ex. "Monday"
    (1, "ddd", "%a"),  # Weekday as locale’s abbreviated name. Ex. "Mon"
    # "": "%w",  # Weekday as a decimal number, where 0 is Sunday and 6 is Saturday. Ex. "1"
    (3, "dd", "%d"),  # Day of the month as a zero-padded decimal number. Ex. "30"
    (4, "d", "%-d"),  # Day of the month as a decimal number. (Platform specific) Ex. "30"
    (5, "MMMM", "%B"),  # Month as locale’s full name. Ex. "September"
    (6, "MMM", "%b"),  # Month as locale’s abbreviated name. Ex. "Sep"
    (7, "MM", "%m"),  # Month as a zero-padded decimal number. Ex. "09"
    (8, "M", "%-m"),  # Month as a decimal number. (Platform specific) Ex. "9"
    (9,"yyyy", "%Y"),  # Year with century as a decimal number. Ex. "2013"
    (10, "y", "%y"),  # Year without century as a zero-padded decimal number. Ex. "13"
    (11, "HH", "%H"),  # Hour (24-hour clock) as a zero-padded decimal number. Ex. "07"
    (12, "H", "%-H"),  # Hour (24-hour clock) as a decimal number. (Platform specific) Ex. "7"
    (13, "hh", "%I"),  # Hour (12-hour clock) as a zero-padded decimal number. Ex. "07"
    (14, "h", "%-I"),  # Hour (12-hour clock) as a decimal number. (Platform specific) Ex. "7"
    (15, "tt", "%p"),  # Locale’s equivalent of either AM or PM. Ex. "AM"
    (16, "mm", "%M"),  # Minute as a zero-padded decimal number. Ex. "06"
    (17, "m", "%-M"),  # Minute as a decimal number. (Platform specific) Ex. "6"
    (18, "ss", "%S"),  # Second as a zero-padded decimal number. Ex. "05"
    (19, "s", "%-S"),  # Second as a decimal number. (Platform specific) Ex. "5"
    (20, "f", "%f"),  # Microsecond as a decimal number, zero-padded on the left. Ex. "000000"
    (21, "zzz", "%Z"),  # Time zone name (empty string if the object is naive). Ex. ""
    (22, "z", "%z"),  # UTC offset in the form +HHMM or -HHMM (empty string if the the object is naive). Ex. ""
    # "": "%j",  # Day of the year as a zero-padded decimal number. Ex. "273"
    # "": "%-j",  # Day of the year as a decimal number. (Platform specific) Ex. "273"
    # "": "%U",
    # Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0. Ex. "39"
    # "": "%W",
    # Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0. Ex. "39"
    (27, "F", "%c"),  # Locale’s appropriate date and time representation. Ex. "Mon Sep 30 07:06:05 2013"
    (28, "D", "%x"),  # Locale’s appropriate date representation. Ex. "09/30/13"
    (29, "T", "%X"),  # Locale’s appropriate time representation. Ex. "07:06:05"
    (30, "Z", "%Y-%m-%dT%H:%m:%s.%f%z")  # Full ISO-8601
]


def _get_now():
    """Gets current date, time and local timezone"""
    return datetime.now(tzlocal())


def _get_now_utc():
    """Gets current UTC date and time"""
    return datetime.utcnow()


def now(*args):
    """Gets current date and time."""
    now = _get_now()
    frmt = None
    if len(args) > 0:
        frmt = args[0]
    return _format(now, frmt)


def now_utc(*args):
    """Gets current UTC date and time."""
    now = _get_now_utc()
    frmt = None
    if len(args) > 0:
        frmt = args[0]
    return _format(now, frmt)


def now_add(*args):
    return "PENDING"


def now_utc_add(*args):
    return "PENDING"


def _format(dt: datetime, format=None):
    """Formats the provided datetime. Default ISO8601+TZ."""
    if format is not None:
        format = _convert_universal_format(format)
        return dt.strftime(format)
    if dt.utcoffset() is None:
        return dt.isoformat() + "-00:00"
    else:
        return dt.isoformat()


def _convert_universal_format(format):
    if "%" in format:
        return format
    else:
        i = 0
        _work_map = _DATETIME_FORMAT_MAP
        for f in _work_map:
            if f[1] in format:
                print(f"-> {format}")
                format = format.replace(f[1], f[2])
                print(f"{f[1]} -> {f[2]} = {format}\n")
                del _work_map[i]
            i += 1

    return format
