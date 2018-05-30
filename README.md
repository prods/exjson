# EXJSON 
## Extended JSON Parser for Python

### Introduction
EXJSON is layer over the Python Standard JSON decoder library, which implements functionality not currently supported by it while trying to keep compliant with the JSON standard as much as possible.

### Main Features
* C Style Single-Line and Multi-Lines Comments.
* Inclusion of other JSON files from local storage or an http/https source.
* Included file checksum verification.
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

The `#Include` directive accepts three parameters from which only the first one is required. They are pipe separated.

```c
#INCLUDE "test.json|{}|e3ae49df2030ee913f8be352999f30d7"
```
- `test.json`: the location of the file to include.
- `{}`: the default value to use if the file is not found and the `error_on_included_file_not_found` is set to `False`.
- `e3ae49df2030ee913f8be352999f30d7`: expected checksum. It will be used in order to verify the file validity.

Additionally you are table to download the file from an http/https url and verify its checksum to prevent injection of malicious code.

**Include from HTTP/HTTPS**
```json
{
  // Sample Property
  "name": "test file",
  // Sample value set with an included object
  "values": [
    /* INCLUDE "http://www.exjson.com/lab/test.json" */
    {
      "value_id": "923ko30k3",
      "value": "Another Value"
    }
  ]
}
```

**Include from HTTP/HTTPS and verify checksum**
```json
{
  // Sample Property
  "name": "test file",
  // Sample value set with an included object
  "values": [
    /* INCLUDE "http://www.exjson.com/lab/test.json|{}|e3ae49df2030ee913f8be352999f30d7" */
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

**Current Limitations**
> **Relative and Absolute Value references are not supported as function parameters yet.**

#### Scripting
EXJSON supports dynamic values by using an extensible scripting engine based on python. Commonly used extension functions can be found in the `scripting/extensions` package but you can create and load your own custom extensions functions by using the `register_custom_scripting_extension`.


- Function calls can be interpolated in strings like `AAX-$.sequence('product-sequence')ZZ` which will yield `AAX-1ZZ`.
- Null values can be set by using `null`.

##### Standard Functions:
###### **Cryptography**
   * **MD5**
     
     Generates a MD5 hash from the specified string value. When no string is provided a random long of 128 random bits is used.
     
   Signature
   ```json
    $.md5([optional]string value)
   ```
     
   Usage
      ```json
      {
        "value": "$.md5('test message')",
        "value1": "$.md5()"
      }
      ```
    Result
      ```json
      {
        "value": "c72b9698fa1927e1dd12d3cf26ed84b2",
        "value1": "a1fa31838987e9a93338afb0831709d7"
      }
      ```
   * **SHA1**
   
     Generates an SHA1 hash from the specified string value. When no string is provided a random long of 128 random bits is used.
     
     Signature
       ```json
        $.sha1([optional]string value)
       ```
     
     Usage
      ```json
      {
        "value": "$.sha1('test message')",
        "value1": "$.sha1()"
      }
      ```
     Result
      ```json
      {
        "value": "35ee8386410d41d14b3f779fc95f4695f4851682",
        "value1": "18ba91517fde987433d27dab5f49390483ac2f03"
      }
      ```
  * **SHA256**
   
     Generates an SHA256 hash from the specified string value. When no string is provided a random long of 256 random bits is used.
     
     Signature
       ```json
        $.sha256([optional]string value)
       ```
     
    Usage
      ```json
      {
        "value": "$.sha256('test message')",
        "value1": "$.sha256()"
      }
      ```
    Result
      ```json
      {
        "value": "3f0a377ba0a4a460ecb616f6507ce0d8cfa3e704025d4fda3ed0c5ca05468728",
        "value1": "c0329b1e9a0b31d62da4855ed3730ad7104a4cd634415b38c038ccaf1db83cc3"
      }
      ```
  * **SHA512**
   
     Generates an SHA512 hash from the specified string value. When no string is provided a random long of 512 random bits is used.
     
     Signature
       ```json
        $.sha512([optional]string value)
       ```
     
    Usage
      ```json
      {
        "value": "$.sha512('test message')",
        "value1": "$.sha512()"
      }
      ```
    Result
      ```json
      {
        "value": "950b2a7effa78f51a63515ec45e03ecebe50ef2f1c41e69629b50778f11bc080002e4db8112b59d09389d10f3558f85bfdeb4f1cc55a34217af0f8547700ebf3",
        "value1": "5ac6b81120595d01cce41f18a14440dffb435955020a682c47288eae9aacf5263a051e14bff01f688433cb575dab0ac82b6135286d0f1ced93dbc37375ffba68"
      }
      ```
###### Date and Time
  
  By default datetime functions will return date and time in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format with explicit TZ even on UTC. ISO-8601 Zulu format can be achived by using the `Z` format as described in the table below:
      
| "Universal" Format Code | [Python Format Code](http://strftime.org/)        | Description                                                      | Example     |
|-------------|---------------------------|------------------------------------------------------------------|-------------|
| dddd        |   %A                      | Weekday as locale’s full name.                                   | Monday      |
| ddd         |   %a                      | Weekday as locale’s abbreviated name.                            | Mon         |
| ww          |   %w                      | Weekday as a zero padded number, where 0 is Sunday and 6 is Saturday.|  01         |
| w           |   %-w                      | Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.|  1          |
| dd          |   %d                      | Day of the month as a zero-padded decimal number.                | 30          |
| d           |   %-d                     | Day of the month as a decimal number.         | 30          |
| MMMM        |   %B                      | Month as locale’s full name.                                     | September   |
| MMM         |   %b                      | Month as locale’s abbreviated name.                              | Sep         |
| MM          |   %m                      | Month as a zero-padded decimal number.                           | 09          |
| M           |   %-m                     | Month as a decimal number.                    |  9          |
| yyyy        |   %Y                      | Year with century as a decimal number.                           | 2013        |
| y           |   %y                      | Year without century as a zero-padded decimal number.            | 13          |
| HH          |   %H                      | Hour (24-hour clock) as a zero-padded decimal number.            | 19          |
| H           |   %-H                     | Hour (24-hour clock) as a decimal number.     | 19          |
| hh          |   %I                      | Hour (12-hour clock) as a zero-padded decimal number.            | 07          |
| h           |   %-I                     | Hour (12-hour clock) as a decimal number.     |  7          |
| tt          |   %p                      | Locale’s equivalent of either AM or PM.                          | AM          |
| mm          |   %M                      | Minute as a zero-padded decimal number.                          | 06          |
| m           |   %-M                     | Minute as a decimal number.                                      |  6          |
| ss          |   %S                      | Second as a zero-padded decimal number.                          | 05          |
| s           |   %-S                     | Second as a decimal number.                   |  5          |  
| f           |   %f                      | Microsecond as a decimal number, zero-padded on the left.        | 000000      |
| zzz         |   %Z                      | Time zone name (empty string if the object is -00:00).           | -04:00      |
| z           |   %z                      | UTC offset in the form +HHMM or -HHMM.                           | -04:00      |
| j           |   %j                      | Day of the year as a zero-padded decimal number.                 | 273         |
| jj          |   %-j                     | Day of the year as a decimal number.          | 273         |
| UU          |   %U                      | Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.        | 09 |
| U           |   %-U                     | Week number of the year (Sunday as the first day of the week) as a decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.        |  9 |
| WW          |   %W                      | Week number of the year (Monday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Monday are considered to be in week 0.                    | 08 |
| W           |   %W                      | Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0.                    |  8 |
| q           |   **custom**              | Calendar Quarter as zero padded number.                           | 04          |
| qq          |   **custom**              | Calendar Quarter as number.                                      |  4          |
| F           |   %c                      | Locale’s appropriate date and time representation.        | Mon Sep 30 07:06:05 2013 |
| D           |   %x                      | Locale’s appropriate date representation.        | 09/30/13 |
| T           |   %X                      | Locale’s appropriate time representation.        | 07:06:05 |
| Z           |   %Y-%m-%dT%H:%m:%s.%f%z  | Zulu UTC ISO-8601                                | 2018-05-25T15:05:25.120Z |
  
  __No need to worry about running it on windows or linux. The universal format converter takes care of the platform specific tokens `-`/`#`.__
    
  
  * **NOW()**
   
     Gets the current date and time based on server timezone.
         
       Signature
       ```json
        $.now([optional]format string)
       ```
         
       Usage
       
          ```json
          {
            "value": "$.now('MM/dd/yyyy hh:mm tt')",
            "value1": "$.now()"
          }
          ```
          
       Result
        
          ```json
          {
            "value": "05/27/2018 12:50 PM",
            "value1": "2018-05-27T12:50:05.302736-04:00"
          }
          ```
  * **NOW().ADD()**
   
     Adds the specified number of time units to the current date and time based on server timezone.
     
       | Unit of Time  |  Description            |
       |------------|-------------------------|
       | day        | Adds or subtracts days. |
       | week       | Adds or subtracts weeks. |
       | month      | Adds or subtracts months. |
       | year       | Adds or subtracts years. |
       | quarter    | Adds or subtracts quarter. |
         
       Signature
       ```json
        $.now().add([required]unit of time criterias..., [optional]format string)
       ```
         
       Usage
       
          ```json
          {
            "value": "$.now().add(day=-1,'MM/dd/yyyy')",
            "value1": "$.now().add(day=-1)"
          }
          ```
          
       Result
        
          ```json
          {
            "value": "05/26/2018",
            "value1": "2018-05-26T00:00:00.0000-04:00"
          }
          ```
      
  * **NOW().UTC()**
  
    Same as `now()` but returns `UTC` date and time.
  
  * **NOW().UTC().ADD()**
  
    Same as `now().add()` but returns `UTC` date and time.
  
* Sequences and Identification
  * **UUID4()**
   
     Returns a uuid v4 hash.
     
      Signature
       ```json
        $.uuid4()
       ```
     
       Usage
       
          ```json
          {
            "value": "$.uuid4()",
          }
          ```
          
       Result
        
          ```json
          {
            "value": "9f1ac603-0e7c-4d25-b73c-05ac2807d814"
          }
          ```
  * **SEQUENCE()**
   
     Creates and returns one or multiple named integer sequence values. Sequences are generated per load/loads call. Sequences are destroyed once they are populated in the JSON file.
         
       Signature
       ```json
        $.sequence([required]sequence_name,  [optional]padding_pattern, [optional]step)
       ```
       The `padding_pattern` uses the [python string formatting mini language](https://docs.python.org/3/library/string.html#formatstrings) and the `step` is defaulted to `1` if no value is provided.
         
       Usage
       
          ```json
          {
            "value": "$.sequence('seq1',2)",
            "values": [
                "test1": "A-$.sequence('seq2', '{0:0>4}')",
                "test2": "A-$.sequence('seq2', '{0:0>4}')"
                "test3": "A-$.sequence('seq2', '{0:0>4}')"
                "test4": "A-$.sequence('seq2', '{0:0>4}')"
            ],
            "value1": "$.sequence('seq1',2)",
          }
          ```
          
       Result
        
          ```json
          {
            "value": "1",
            "values": [
                "test1": "A-0001",
                "test2": "A-0002"
                "test3": "A-0003"
                "test4": "A-0004"
            ],
            "value1": "1",
          }
          ```
  * **FILE_CHECKSUM()**
   
     Calculates MD5 or SHA1 checksum for the specified file. The file path should be relative to the path where the JSON file is located if loaded or included. Relative to the executing python script if using loads from a JSON string. If no `algorithm` is provided `md5` will be used by default.
         
       Signature
       ```json
        $.file_checksum([required]file_path,  [optional]algorithm)
       ```
       Supported algorithms are `md5` and `sha1`.
       
       Usage
       
          ```json
          {
            "filename": "../file.db",
            "checksum": "$.file_checksum('../file.db', 'md5')"
          }
          ```
          
       Result
        
          ```json
           {
            "filename": "../file.db",
            "checksum": "ceb4c1f4b28bd59b941573d8a41f14d3"
          }
          ```

##### How to Create a custom scripting extension function and register it at Run-Time.
While standard functions can be added through issues (requests) or pull requests into the version branch you may want to use some functions that are too specific to your scenario that cannot be classified as standard. In this case you may want to register them at run-time.

Standard or Custom Scripting Extension Function Example:
```python
def custom_add(*args):
    result = 0
    if len(args) == 0:
        result = 0
    else:
        for r in args:
            result = result + r
    return result
```
A custom scripting function should always have an `*args` variable in order to allow for an undefined number of parameters to be passed in. Parameter check can always be performed inside the function body if required. The scripting extension functio should always return a primitive type (`int`, `str`, `float`, etc...). Arrays and other types are not supported yet.

Registration:
```python
if __name__ == "__main__":
    exjson.register_custom_scripting_extension("add", custom_add)
    ...
    exjson.load("sample.json")
```

Usage:
```json
{
  "a": $.add(10, 20)
}
```

Result:
```json
{
  "a": 30
}
```

The resulting value can be accessed using the relative and absolute accessors `$this`, `$parent` and `$root` from anywhere in the current file or an included JSON file. 

### Life Cycle:

1. Load JSON File Content
2. Comments are extracted.
3. Directives are extracted from comments.
4. Include files (`#INCLUDE` directive) content are extracted recursively (Apply steps 1 to 4). 
   The load process is stopped if an included file is determined to have a circular reference.
5. Include files are merged into JSON file which included it.
6. Script function calls are extracted and evaluated.
7. Relative and Absolute value references are evaluated.


### Unit Test Requirements:
EXJSON unit testing runs on the [standard Python unit test library](https://docs.python.org/2/library/unittest.html). But I EXJSON unit test functions support automatic-generation of call diagrams from each test function execution. Because of this there is an additional dependency on [PyCallGraph](http://pycallgraph.readthedocs.io/en/master/). Please follow the steps below in order to install this dependency on Windows, Linux or OSX.
Please bear in mind that the steps below assume you already have python 3.6+ and pip installed. Depending on how your environment is setup Python 3.x `pip` may be available through an alias named `pip3`.

#### Turn on and off call graph generator
Call graph generate is controlled by an environmental variable named `GENERATE_CALL_GRAPHS`. If the environmental variable does not exists the value is defaulted to `False`, no graph will be generated. If it exists and it is set to `True` graphs will be generated in the `tests/calls` folder.

**Linux/OSX**
```bash
export GENERATE_CALL_GRAPHS=True
```

**Windows**
```cmd
%GENERATE_CALL_GRAPHS%=True
```

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
* Better unit testing coverage.
* Stabilize and resolve any bugs.
* Segregate and make better scripting extension documentation.
* Support Multi-File Serialization.
* For More check [Issues](https://github.com/prods/exjson/issues) tagged as `next release` or `deffered` for details.
