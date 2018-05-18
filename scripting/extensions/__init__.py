from scripting.extensions.exs_crypt import _exjson_uuid, _exjson_md5, _exjson_sha1, _exjson_sha256, _exjson_sha512
from scripting.extensions.exs_datetime import _exjson_now, _exjson_now_add, _exjson_now_utc, _exjson_now_utc_add

# Functions Dict
# This is ok for now since the list of functions is simple enough. But further refactoring may be required
_functions = {
    "$.now": _exjson_now,
    "$.now().add": _exjson_now_add,
    "$.now().utc": _exjson_now_utc,
    "$.now().utc().add": _exjson_now_utc_add,
    "$.uuid": _exjson_uuid,
    "$.md5": _exjson_md5,
    "$.sha1": _exjson_sha1,
    "$.sha256": _exjson_sha256,
    "$.sha512": _exjson_sha512
}


def get_function(func_call):
    fn_key = func_call[:func_call.rfind('('):]
    fn_parameters_str = func_call[func_call.rfind('(') + 1:func_call.rfind(')')]
    fn_parameters = [remove_quotation(v) for v in fn_parameters_str.split(",")]
    if fn_key in _functions.keys():
        return (_functions[fn_key], fn_parameters)


def remove_quotation(value):
    result = value
    if value.startswith("\'") or value.startswith("\""):
        result = result[1:]
    if value.endswith("\'") or value.endswith("\""):
        result = result[:-1]
    return result