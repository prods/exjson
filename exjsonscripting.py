import hashlib
import random
import uuid
from datetime import datetime, timedelta
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
    return now.isoformat() + "Z"


def _exjson_now_add(*args, **kwargs):
    return "PENDING"


def _exjson_now_utc_add(*args, **kwargs):
    return "PENDING"


def _exjson_uuid(*args, **kwargs):
    return str(uuid.uuid4())


def _exjson_md5(*args, **kwargs):
    value = ""
    if len(args) > 0:
        value = args[0]
    elif len(args) == 0 and "value" in kwargs.keys():
        value = kwargs["value"]
    if value is None or value == "":
        value = str(random.getrandbits(128)).encode('utf-8')
    return hashlib.md5(value).hexdigest()


def _exjson_sha1(*args, **kwargs):
    value = ""
    if len(args) > 0:
        value = args[0]
    elif len(args) == 0 and "value" in kwargs.keys():
        value = kwargs["value"]
    if value is None or value == "":
        value = str(random.getrandbits(128)).encode('utf-8')
    return hashlib.sha1(value).hexdigest()


def _exjson_sha256(*args, **kwargs):
    value = ""
    if len(args) > 0:
        value = args[0]
    elif len(args) == 0 and "value" in kwargs.keys():
        value = kwargs["value"]
    if value is None or value == "":
        value = str(random.getrandbits(256)).encode('utf-8')
    return hashlib.sha256(value).hexdigest()


def _exjson_sha512(*args, **kwargs):
    value = ""
    if len(args) > 0:
        value = args[0]
    elif len(args) == 0 and "value" in kwargs.keys():
        value = kwargs["value"]
    if value is None or value == "":
        value = str(random.getrandbits(512)).encode('utf-8')
    return hashlib.sha512(value).hexdigest()


_functions = {
    "$.now": _exjson_now,
    "$.now().add": _exjson_now_add,
    "$.now().utc": _exjson_now_utc,
    "$.now().utc().add": _exjson_now_utc_add,
    "$.uuid": _exjson_uuid,
    "$.md5": _exjson_md5,
    "$.sh1": _exjson_sha1,
    "$.sha256": _exjson_sha256,
    "$.sha512": _exjson_sha512
}

def parse(source, raise_error_on_invalid_value=False):
    if "$." not in source:
        return source
    calls = {}
    updated_source = source
    for line in source.splitlines():
        c = 0
        while c < len(line):
            if line[c] == "$":
                call_close = c + 1
                call_params = ""
                while line[call_close] == ".":
                    call_close = line.find(")", call_close + 1) + 1
                if call_close > 0:
                    key = line[c:call_close]
                    fn_key = key[:key.rfind('('):]
                    fn_parameters = key[key.rfind('(')+1:key.rfind(')')]
                    if fn_key in _functions.keys():
                        calls[key] = (_functions[fn_key], fn_parameters)
                    c += call_close
            c += 1
    for fn_key in calls.keys():
        #print(f"KEY: {fn_key}\nFN: {calls[fn_key]}\nCALL: {calls[fn_key][0].__name__}\nPARAMS: {calls[fn_key][1]}\nRESULT: {calls[fn_key][0](calls[fn_key][1])}\n---------\n")
        updated_source = updated_source.replace(fn_key, calls[fn_key][0](calls[fn_key][1]))
    return updated_source