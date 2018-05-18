import hashlib
import random
import uuid


def _exjson_uuid(*args):
    return str(uuid.uuid4())


def _exjson_md5(*args):
    value = ""
    if len(args) > 0:
        value = args[0]
    if value == "":
        value = str(random.getrandbits(128))
    return hashlib.md5(value.encode('utf-8')).hexdigest()


def _exjson_sha1(*args):
    value = ""
    if len(args) > 0:
        value = args[0]
    if value == "":
        value = str(random.getrandbits(128))
    return hashlib.sha1(value.encode('utf-8')).hexdigest()


def _exjson_sha256(*args):
    value = ""
    if len(args) > 0:
        value = args[0]
    if value == "":
        value = str(random.getrandbits(256))
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def _exjson_sha512(*args):
    value = ""
    if len(args) > 0:
        value = args[0]
    if value == "":
        value = str(random.getrandbits(512))
    return hashlib.sha512(value.encode('utf-8')).hexdigest()