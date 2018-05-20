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
        if hasattr(calls[fn_key][0], "__isolated_instance_execution__") and calls[fn_key][0].__isolated_instance_execution__:
            i = 0
            new_updated_source = ""
            for call_instance in updated_source.split(fn_key):
                if i == 0:
                    updated_instance = call_instance
                else:
                    updated_instance = str(calls[fn_key][0](*calls[fn_key][1])) + call_instance
                new_updated_source += updated_instance
                i += 1
            updated_source = new_updated_source
            # Call Close Function for the Extension call
            if hasattr(calls[fn_key][0], "__close__") and calls[fn_key][0].__close__ is not None:
                calls[fn_key][0].__close__()
        else:
            updated_source = updated_source.replace(fn_key, str(calls[fn_key][0](*calls[fn_key][1])))
    return updated_source