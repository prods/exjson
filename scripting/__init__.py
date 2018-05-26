import re

from scripting import extensions

_REF_PREFIXES = ['$this.', '$parent.', '$root.']


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


def _parse_reference_calls(source: str):
    """Parses reference calls"""
    updated_source = source
    # Extract Source Tree and Reference Tree
    base = _extract_tree(updated_source)
    # Source Tree
    source_tree = base[0]
    # References Tree
    ref_calls = base[1]
    print(source_tree)
    print(ref_calls)
    if ref_calls is not None and len(ref_calls) > 0:
        for r in ref_calls:
            print(ref_calls[r])
            updated_source = updated_source.replace(r, source_tree[ref_calls[r]])
            # Update Tree when a value ref_call is updated. This guarantees references of references to get the initially referenced value.
            source_tree = _extract_tree(updated_source, extract_ref_calls=False)[0]
    return updated_source


def _extract_tree(source: str, outer_tree: dict = None, extract_ref_calls: bool = True):
    tree = {}
    ref_tree = {}
    if outer_tree is not None:
        tree = {**outer_tree}
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
                inner_object_tree = _extract_tree(source_value, tree)
                for inner_object_key in inner_object_tree[0]:
                    tree[f"{source_key}.{inner_object_key}"] = inner_object_tree[0][inner_object_key]
                    # Extract Ref Tree
                    if extract_ref_calls:
                        if inner_object_tree[1] is not None:
                            for k in inner_object_tree[1]:
                                if k not in ref_tree:
                                    ref_tree[k] = inner_object_tree[1][k]
            # Set the Value
            tree[source_key] = source_value
            # Extract References
            if extract_ref_calls:
                ref_call = _extract_ref_call(source_value, tree.keys())
                # if ref_call is not None:
                #    print(f"|{ref_call[1]}| IN {[x for x in tree.keys()]}")
                if ref_call is not None and ref_call[1] in tree.keys():
                    if ref_call[0] not in ref_tree:
                        # print(f">>>  |{ref_call}| IN {[x for x in ref_tree.keys()]}")
                        ref_tree[ref_call[0]] = ref_call[1]
            # Reset
            working_source = working_source[i + source_value_end_index:]
            i = 0
            continue
        # Next Character
        i = i + 1
    # Debug
    # for r in tree:
    #    print(f"> {r} = {tree[r]}\n")
    return (tree, ref_tree)


def _extract_ref_call(source: str, keys: list):
    if "$this." in source or "$parent." in source or "$root." in source:
        ref_start = -1
        ref_prefix_end = -1
        ref_call_without_prefix = ""
        ref_call_prefix = ""
        for i in range(len(source)):
            if source[i] == "$":
                ref_start = i
                ref_prefix_end = source[i:].index(".") + 1
                ref_call_prefix = source[i:ref_prefix_end - 1]
            if ref_start >= 0:
                if ref_call_without_prefix not in keys:
                    if ref_prefix_end > 0 and i >= ref_prefix_end:
                        if source[i] in ['"']:
                            break
                        ref_call_without_prefix = ref_call_without_prefix + source[i]
                else:
                    break
        print(f">>>>> {ref_call_without_prefix}")
        if ref_call_prefix != "" and ref_call_without_prefix != "":
            ref_call = f"{ref_call_prefix}.{ref_call_without_prefix}"
            return (ref_call, ref_call_without_prefix, ref_call_prefix)
        else:
            return None
    else:
        return None
