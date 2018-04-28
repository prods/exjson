# XJSON (Extensible JSON)

*This Project is currently in Alpha State.*

### Introduction
This project was born as part of a toolset require for another project I am working on. Its main purpose is to provide an simple api to support extending the functionality of the python standard library json parser. 

### API
The XJson API partially supports the standard json library functions for inplace replacement, if you only use loads() and dumps(). Some extended functionality may not be supported on all functions due to the need of specific parameters not supported by the standard library json library function signatures.

* loads()
  - Supports #INCLUDE directive.
  - Supports single-line and multi-line C style comments
* dumps()
  - Does not support #INCLUDE directive.
  - Does not support comments in general.

Extended Features:
 * C Style Include directive
 Loads specified file from the same path where the file is being loaded.
 Supports two syntaxes:
 ```c
#INCLUDE < secondary.json >
```
or
 ```c
#INCLUDE "secondary.json"
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


Road Map:
* Value Reference from same or different file. Accessible by JSON tree.
* Basic Scripting. Dynamic values support.
* Support Include persistence by using `__xjson_single__ = True` property
