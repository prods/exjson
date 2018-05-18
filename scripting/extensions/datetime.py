from datetime import datetime

from dateutil.tz import tzlocal


def _get_now():
    """Gets current date, time and local timezone"""
    return datetime.now(tzlocal())

def _get_now_utc():
    """Gets current UTC date and time"""
    return datetime.utcnow()

def now(*args):
    """Gets current date and time. Default format is ISO8601+TZ."""
    now = _get_now()
    if len(args) > 0:
        return now.strftime(args[0])
    return now.isoformat()


def now_utc(*args):
    """Gets current UTC date and time. Default format is ISO8601+TZ."""
    now = _get_now_utc()
    if len(args) > 0:
        return now.strftime(args[0])
    return now.isoformat() + "-00:00"


def now_add(*args):
    return "PENDING"


def now_utc_add(*args):
    return "PENDING"