import re

from scripting import extensions

_REF_VALUE_CALL = re.compile(r'\$this\.(.*)|\$parent\.(.*)|\$_\.(.*)|\$root\.(.*)',
                             re.IGNORECASE | re.MULTILINE)


def parse(source, raise_error_on_invalid_value=False):
    if "$." not in source:
        return _parse_reference_calls(source)
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
        if hasattr(calls[fn_key][0], "_isolated_instance_execution") and calls[fn_key][0]._isolated_instance_execution:
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
            if hasattr(calls[fn_key][0], "_close") and calls[fn_key][0]._close is not None:
                calls[fn_key][0]._close()
        else:
            updated_source = updated_source.replace(fn_key, str(calls[fn_key][0](*calls[fn_key][1])))
    # Parse Reference Calls
    updated_source = _parse_reference_calls(updated_source)
    # Result
    return updated_source


def _parse_reference_calls(source):
    """Parses reference calls"""
    updated_source = source
    source_data_map = _extract_data_map(updated_source)
    ref_calls = re.finditer(_REF_VALUE_CALL, updated_source)
    for match_num, match in enumerate(ref_calls):
        if len(match.groups()) > 0:
            for value in match.groups():
                if value is None:
                    continue
                ref_call = str(match.group())
                ref_call = _get_ref_call(ref_call)
                ref_call_key = ref_call.replace("$this.", "").replace("$root.", "").replace("$parent.", "")
                if ref_call_key in source_data_map.keys():
                    updated_source = updated_source.replace(ref_call, source_data_map[ref_call_key])
    return updated_source


def _extract_data_map(source):
    tree = {}
    i = 0
    done = False
    working_source = source
    while not done:
        # Done
        if i == len(working_source):
            done = True
            continue
        # Find property assignments
        if working_source[i] == ":":
            source_key_start_index = 0
            source_value_end_index = 0
            source_key = ""
            source_value = ""
            source_key_scope = working_source[:i]
            try:
                source_key_start_index = source_key_scope.rindex(',')
            except:
                source_key_start_index = source_key_scope.rindex("{")
            source_key = source_key_scope[source_key_start_index:].replace('"', '').replace(' ', '').replace('\t',
                                                                                                             '').replace(
                '\n', '').replace('{', '').replace(',', '')
            source_value_scope = working_source[i:]
            # Find arrays
            if source_value_scope.replace(' ', '').replace('\t', '')[1] == '[':
                source_value_end_index = source_value_scope.index("]") + 1
            elif source_value_scope.replace(' ', '').replace('\t', '')[1] == "{":
                source_value_end_index = source_value_scope.index("}") + 1
            else:
                try:
                    source_value_end_index = source_value_scope.index(",")
                except:
                    source_value_end_index = source_value_scope.index("}")
            source_value = source_value_scope[1:source_value_end_index].strip(' ').strip('\t').strip('"')
            # Process Object
            if source_value[0] == "{" and source_value[-1] == "}":
                inner_object_tree = _extract_data_map(source_value)
                for inner_object_key in inner_object_tree:
                    tree[f"{source_key}.{inner_object_key}"] = inner_object_tree[inner_object_key]
            # Set the Value
            tree[source_key] = source_value
            # Reset
            working_source = working_source[i + source_value_end_index:]
            i = 0
            continue
        # Next Character
        i = i + 1
    # Debug
    #for r in tree:
    #    print(f"> {r} = {tree[r]}\n")
    return tree


def _get_ref_call(ref_call):
    result = ""
    for c in ref_call:
        if c in [" ", "\'", "\"", ";", ",", "|", "-"]:
            break
        result += c
    return result
