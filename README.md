# EXJSON 
## Extended JSON Parser for Python

*This Project is under active development and it is not ready for production*

### Introduction
EXJSON is layer over the Python Standard JSON decoder library, which implements functionality not currently supported by it while trying to keep compliant with the JSON standard as much as possible.

### Main Features
* C Style Single-Line and Multi-Lines Comments.
* Inclusion of other JSON files.
* Absolute and Relative Value referencing using `$root`, `$parent` and `$this`.
* Extensible Scripting.


### Supported Python Versions
- Python 3.x

### Install/Upgrade

```sh
pip install exjson --upgrade
```

### Sample

**samplefile1.json**
```json
{
  // Sample Property
  "name": "test file",
  // Sample value set with an included object
  "values": [
    /* INCLUDE "samplefile2.json" */
    {
      "value_id": "923ko30k3",
      "value": "Another Value"
    }
  ]
}
```

**samplefile2.json**
```json
/*
  INCLUDIBLE TEST FILE
*/
{
   "value_id": "93987272",
   "value": "This Value"
}
```

**Usage**
```python
import exjson as json

# Decode
sample_value_set = json.load("./samplefile1.json")

# ... Do stuff with sample_value_set

# Encode
with open("./result.json") as f:
    f.write(json.dumps(sample_value_set))

```

**result.json**
```json
{
  "name": "test file",
  "values": [
    {
       "value_id": "93987272",
       "value": "This Value"
    },
    {
      "value_id": "923ko30k3",
      "value": "Another Value"
    }
  ]
}
```

For more complex examples please check the [unit tests](https://github.com/prods/exjson/tree/master/tests).


### API
The exjson API offers similar API to the one available on the Python standard JSON decoder/encoder library. 

* **load**(json_file_path, encoding=None, cls=None, object_hook=None, parse_float=None,
          parse_int=None, parse_constant=None, object_pairs_hook=None, error_on_include_file_not_found=False, \*\*kw)
          
  Deserializes JSON file into a dictionary.
          
  **Arguments:**
  - `json_file_path`: main json file to be loaded.
  - `encoding`: encoding codec to use when loading the file and all included files. All included files should use the same encoding.
  - `cls`: if specified, it uses the provided custom JSONDecoder instance to decode the json file. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `object_hook`: if specified, it will be called for every decoded JSON object and its value will be used instead of the default `dict`. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `parse_float`: if specified, it will be called for every `float` that is decoded. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `parse_int`: if specified, it will be called for every `int` that is decoded. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `parse_constant`: if specified, will be called with one of the following strings: '-Infinity', 'Infinity', 'NaN'. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `object_pairs_hook`: if specified, it will be called for every decoded JSON object with an ordered list of pairs. Its result will be used instead of the default `dict`. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `error_on_included_file_not_found`: if set to `True` an Exception is raised if an included file is not found.
  
  **Supported Extended Functionality:**
   - Supports #INCLUDE directive. 
   - Supports single-line and multi-line C style comments
  
* **loads**(json_string, encoding=None, cls=None, object_hook=None, parse_float=None,
          parse_int=None, parse_constant=None, object_pairs_hook=None, error_on_include_file_not_found=False, includes_path=None, \*\*kw)
  
  Deserializes JSON string into a dictionary.
          
  **Arguments:**
  - `json_file_path`: main json file to be loaded.
  - `encoding`: encoding codec to use when loading the file and all included files. All included files should use the same encoding.
  - `cls`: if specified, it uses the provided custom JSONDecoder instance to decode the json file. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `object_hook`: if specified, it will be called for every decoded JSON object and its value will be used instead of the default `dict`. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `parse_float`: if specified, it will be called for every `float` that is decoded. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `parse_int`: if specified, it will be called for every `int` that is decoded. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `parse_constant`: if specified, will be called with one of the following strings: '-Infinity', 'Infinity', 'NaN'. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `object_pairs_hook`: if specified, it will be called for every decoded JSON object with an ordered list of pairs. Its result will be used instead of the default `dict`. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONDecoder)
  - `error_on_included_file_not_found`: if set to `True` an Exception is raised if an included file is not found.
  - `includes_path`: if provided it will be used to set the root path from where the included files will be loaded. When not provided the executing python script path will be used. Please, bear in mind that `#INCLUDE` directive file path is consider relative to this one.
  
  **Supported Extended Functionality:**
   - Supports #INCLUDE directive. 
   - Supports single-line and multi-line C style comments
   
* **dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=True, cls=None, indent=None, separators=None,
          default=None, sort_keys=False, \*\*kw)**
  
  Serializes a python object/dictionary instance into a JSON string.
  
  **Arguments:**
  - `obj`: object instance to encode (serialize).
  - `skipkeys`: If set to `False` a `TypeError` is raised if the keys are not primitive types (`int`, `str`, `float` or `None`). [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONEncoder)
  - `ensure_ascii`: If set to `True` all Incoming ASCII characters will be escaped in the output, else they will kept as-is. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONEncoder)
  - `check_circular`: If set to `True` will check all classes and dictionaries for prevent circular references in order to prevent infinite recursion. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONEncoder)
  - `allow_nan`: If set to `True`, `NaN`, `Infinity`, and `-Infinity` will be encoded as such. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONEncoder)
  - `cls`: [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONEncoder)
  - `indent`: If set to `True` the output json will be indented. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONEncoder)
  - `separators`: If specified, it should be a tuple listing the item and key separators to use during encoding. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONEncoder)
  - `default`: [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONEncoder.default)
  - `sort_keys`: It set to `True` the output dictionary will be sorted by key. [See Python docs for details.](https://docs.python.org/3/library/json.html#json.JSONEncoder)
          
  **Supported Extended Functionality:**
  - Does not support #INCLUDE directive.
  - Does not support comments.

### Features:

#### C Style Comments
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


#### C Style Include directive
 Loads specified file from the same path where the file is being loaded.
 Supports 2 syntax always enclosed in comments:
 
 ```c
 /* #INCLUDE <[PropertyName:]json_file_relative_path> */
 ```
 
 **PropertyName** _(Optional)_
 
 This is the name of the JSON property that will encapsulate the included file content. This required when including a file between other properties.
 
 
 ```json
 {
  "Name": "Test"
  /* #INCLUDES <Values:values.json> */
 }
 ```
 
 ```json
 {
  "Name": "Test",
  "Values": { 
    "1": "Test1",
    "2": "Test2"
   }
 }
 ```
 
**json_file_relative_path** 
 
This is the json file name including relative path (if located in a nested folder) to the path where the main json file exists. When the main json is loaded as a string and the `includes_path` is not specified it will use the executing python script path.
If the script is not found an error will be raised.
 

The `#INCLUDE` directive arguments can be enclosed in `<>` or `""`.


#### Access Value by Reference
`$root`, `$parent` and `$this` accessor prefixes are supported. This accessors allow you to reference values from the JSON root, parent or current object even if they are being included or its value is being calculated at runtime using a function and they can be interpolated into a string without the need of enclosing characters.

Sample:
```json
{
  "prefix": "A",
    "first": [
        { "id": "A1" },
        { "id": "A2" },
        { "id": "A3" },
        { "id": "$root.prefix4" }
    ],
    "second": "$root.prefix",
    "third": {
        "test1": 23,
        "test2": [
            1,2,3
        ],
        "test3": {
            "deep1": 44,
            "deep2": false,
            "deep3": "$root.secondB",
            "deep4": "AZ-$parent.test1X"
        }
    },
    "fourth": {
      "t1": "B",
      "t2": "$this.t1"
    }
}
```

Result:
```json
{
  "prefix": "A",
    "first": [
        { "id": "A1" },
        { "id": "A2" },
        { "id": "A3" },
        { "id": "A4" }
    ],
    "second": "A",
    "third": {
        "test1": 23,
        "test2": [
            1,2,3
        ],
        "test3": {
            "deep1": 44,
            "deep2": false,
            "deep3": "AB",
            "deep4": "AZ-23X"
        }
    },
    "fourth": {
      "t1": "B",
      "t2": "B"
    }
}
```

 * **first[3]** = `$root.prefix4` references the value of `prefix` on the JSON root while interpolated in the string.
 * **second** = `$root.prefix` references the value of `prefix` on the JSON root.
 * **third.test3.deep3** = `$root.secondB` referenced the value of `second` on the JSON root while interpolated in the string.
 * **third.test3.deep4** = `AZ-$parent.test1X` references the the value of `$root.third.test1` which is the parent object of `test3` while interpolated in a string.
 * **fourth.t2** = `$this.t1` references the value of `$root.fourth.t1` which is the parent


#### Scripting
EXJSON supports dynamic values by using an extensible scripting engine based on python. Commonly used extension functions can be found in the `scripting/extensions` package but you can create and load your own custom extensions functions by using the `mount_extension` function.

Standard Functions:
* Cryptography
  - $.md5(str)
  - $.sha1(str)
  - $.sha256(str)
  - $.sha512(str)
* Date and Time
  - $.now()
  - $.now().add()
  - $.now().utc()
  - $.now().utc().add()
* Sequences and Identification
  - $.uuid4()
  - $sequence

##### How to create and register a custom extension function
** PENDING **


### How does it work:

#### Deserialization
It uses CPython if available or the Standard Python JSON parser library if not available.

#### Includes
The `#INCLUDE <*>` directives are identified in the file and the file name enclosed in `< >` or `" "` is extracted. Then the XJson include logic looks for the file in the same path where the main json file is located. Once the file is found the file content is loaded and placed in the location where the `#INCLUDE` directive was located. If the file is not found the `#INCLUDE` directive is ignored and removed when all comments are dropped or an exception can be raised if the `error_on_include_file_not_found` argument is set to `True` when calling `loads()`. Another cool behavior of the include functionality is that it will automatically add a comma at the end of the `#INCLUDE` if it determines that the json file was included in a location where it is followed by more json content. This allows makes it simple to include files without worrying about where it should go.

**It is not recommended to included JSON files that are full and valid json. This make it easy to validate in isolation. Never #INCLUDE a partial json that cannot be validated by itself... but you can...** 

#### C Style Comments
Its simple. Comments are removed in memory before deserialization. This allows the Standard Python JSON parser deserialize the JSON file.

### Unit Test Requirements:
EXJSON unit testing runs on the [standard Python unit test library](https://docs.python.org/2/library/unittest.html). But I EXJSON unit test functions support automatic-generation of call diagrams from each test function execution. Because of this there is an additional dependency on [PyCallGraph](http://pycallgraph.readthedocs.io/en/master/). Please follow the steps below in order to install this dependency on Windows, Linux or OSX.
Please bear in mind that the steps below assume you already have python 3.6+ and pip installed. Depending on how your environment is setup Python 3.x `pip` may be available through an alias named `pip3`.

#### Ubuntu
1. Install `Graphviz` and it's development libraries
```bash
sudo apt-get install graphviz libgraphviz-dev
```
2. Install `pygraphviz`
```bash
pip install pygraphviz
``` 
4. Install `pycallgraph`.
```bash
pip install pycallgraph
```

Alternatively you can download the [PyGraphviz](https://pypi.org/project/graphviz/#files) wheel file from Pypi.org and installing it as described in steps 4 and 5 for Windows below.

### Windows
1. Download [Graphviz for windows](https://graphviz.gitlab.io/_pages/Download/Download_windows.html) from the graphiviz site.
2. Add the Graphviz bin path `C:\Program Files (x86)\Graphviz2.38\bin` in your Windows path.
3. **Close and reopen your terminals so the path changes is recognized.**
4. Download the [pygraphviz python 3.6 wheel](https://pypi.org/project/graphviz/#files).
5. Install the `pygraphviz` wheel.
  ```bash
  pip install graphviz-0.8.3-py2.py3-none-any.whl
  ``` 
6. Install `pycallgraph`
```bash
pip install pycallgraph
```

### OSX
1. Install [HomeBrew](https://brew.sh/).
2. Download the [pygraphviz python 3.6 wheel](https://pypi.org/project/graphviz/#files).
3. Install the `pygraphviz` wheel.
```bash
pip install graphviz-0.8.3-py2.py3-none-any.whl
``` 
4. Install `pycallgraph`.
```bash
pip install pycallgraph
```

### Road Map:
* Value Reference from same or different file. Accessible by using dot notation on JSON properties tree.
* Basic Scripting. Dynamic values support. Example: UUID, Enumeration, Date Calculation and formatting.
* Support serialization to multiple files by using `__exjson_file__ = "filename.json"` property and creation of `#INCLUDE` directives.
* Support for class `docstring` comments usage as json comments during serialization.
