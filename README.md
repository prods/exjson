# XJSON (eXtended JSON)

*This Project is currently in Alpha State.*

### Introduction
This project was born as part of a toolset I required for another project of mine. XSJON is layer over the Python Standard JSON decoder library, which implements functionality not currently supported by it while trying to keep compliant with the JSON standard as much as possible. One important premise is to allow for an in place replacement of the Python Standard JSON decoder for easy migration/replacement.  

### Supported Python Versions
- Python 3.x

### API
The XJson API partially supports the standard json library functions for in place replacement, if you only use loads() and dumps(). Some extended functionality may not be supported on all functions due to the need of specific parameters not supported by the standard library json library function signatures.

* [**loads(json_file_path, encoding=None, cls=None, object_hook=None, parse_float=None,
          parse_int=None, parse_constant=None, object_pairs_hook=None, error_on_include_file_not_found=False, \*\*kw)**](https://docs.python.org/3/library/json.html#json.load)
  - Supports #INCLUDE directive. if `error_on_include_file_not_found` is set to `True` an exception is thrown if an included file is not found.
  - Supports single-line and multi-line C style comments
* [**dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=True, cls=None, indent=None, separators=None,
          default=None, sort_keys=False, \*\*kw)**](https://docs.python.org/3/library/json.html#json.dump)
  - Does not support #INCLUDE directive.
  - Does not support comments.

### Extended Features:
 * C Style Include directive
 Loads specified file from the same path where the file is being loaded.
 Supports 2 syntax always enclosed in comments:
 ```c
/* #INCLUDE <_secondary.json> */

// #INCLUDE <_secondary.json>

/* #INCLUDE "_secondary.json" */

// #INCLUDE "_secondary.json"
```

* C Style Comments
Supports C Style Comments.
Single-Line
```c
// TEST

/* TEST */
```

```c
/* 
TEST
*/
```

### How it works:

#### Deserialization
It uses CPython if available or the Standard Python JSON parser library if not available.

#### Includes
The `#INCLUDE <*>` directives are identified in the file and the file name enclosed in `< >` or `" "` is extracted. Then the XJson include logic looks for the file in the same path where the main json file is located. Once the file is found the file content is loaded and placed in the location where the `#INCLUDE` directive was located. If the file is not found the `#INCLUDE` directive is ignored and removed when all comments are dropped or an exception can be raised if the `error_on_include_file_not_found` argument is set to `True` when calling `loads()`. Another cool behavior of the include functionality is that it will automatically add a comma at the end of the `#INCLUDE` if it determines that the json file was included in a location where it is followed by more json content. This allows makes it simple to include files without worrying about where it should go.

**It is not recommended to included JSON files that are full and valid json. This make it easy to validate in isolation. Never #INCLUDE a partial json that cannot be validated by itself... but you can...** 

#### C Style Comments
Its simple. Comments are removed in memory before deserialization. This allows the Standard Python JSON parser deserialize the JSON file.

### Road Map:
* More unit tests
* Value Reference from same or different file. Accessible by JSON property tree.
* Basic Scripting. Dynamic values support. Example: Date Calculation and formatting.
* Support serialization to multiple files by using `__xjson_file__ = "filename.json"` property.
* Benchmarking?

