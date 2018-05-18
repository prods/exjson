from scripting import extensions


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
                    func_call = line[c:call_close]
                    calls[func_call] = extensions.get_function(func_call)
                    c += call_close
            c += 1
    for fn_key in calls.keys():
        #print(f"KEY: {fn_key}\nFN: {calls[fn_key]}\nCALL: {calls[fn_key][0].__name__}\nPARAMS: {calls[fn_key][1]}\nRESULT: {calls[fn_key][0](calls[fn_key][1])}\n---------\n")
        updated_source = updated_source.replace(fn_key, calls[fn_key][0](calls[fn_key][1]))
    return updated_source