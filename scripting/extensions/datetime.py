from datetime import datetime

from dateutil.tz import tzlocal


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


def _format(dt:datetime, format = None):
    """Formats the provided datetime. Default ISO8601+TZ."""
    if format is not None:
        return dt.strftime(format)
    if dt.utcoffset() is None:
        return dt.isoformat() + "-00:00"
    else:
        return dt.isoformat()