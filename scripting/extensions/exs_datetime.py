from datetime import datetime

from dateutil.tz import tzlocal


def _get_now():
    return datetime.now(tzlocal())

def _get_now_utc():
    return datetime.utcnow()

def _exjson_now(*args, **kwargs):
    now = _get_now()
    if len(args) > 0:
        now.strftime(args[0])
    elif len(args) == 0 and "format" in kwargs.keys():
        now.strftime(kwargs["format"])
    return now.isoformat()


def _exjson_now_utc(*args, **kwargs):
    now = _get_now_utc()
    if len(args) > 0:
        now.strftime(args[0])
    elif len(args) == 0 and "format" in kwargs.keys():
        now.strftime(kwargs["format"])
    return now.isoformat() + "-00:00"


def _exjson_now_add(*args, **kwargs):
    return "PENDING"


def _exjson_now_utc_add(*args, **kwargs):
    return "PENDING"