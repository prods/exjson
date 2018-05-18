import hashlib
import random
import uuid


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