[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PyPI Latest Release](https://img.shields.io/pypi/v/miller.svg)](https://pypi.org/project/miller/) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Documentation Status](https://readthedocs.org/projects/miller/badge/?version=latest)](http://miller.readthedocs.io/?badge=latest)

# What is miller?

*"I'm a tool that finds things."* - Detective Josephus Miller

Named after the erstwhile inspector from *The Expanse*, this package provides convenient, simple introspection tools for packages, modules, classes, objects, attributes, and containers. 

# Why miller?

## Universal

Consider the different and often difficult-to-read syntax that Python uses for introspection of different objects.
```
"""Returns a list of function names in the module 'item'."""
[m[0] for m in inspect.getmembers(item, inspect.isfunction)
 if m[1].__module__ == item.__name__]
"""Returns names of properties of the instance 'item'."""
[a for a in dir(item) if isinstance(getattr(a, item), property)] 
"""Returns names of fields of the dataclass 'item'."""
[f.name for f in dataclasses.fields(item)] 
```
That code can be difficult to remember, requires importing a range of packages, and is not easy to understand if you are not familiar with the relevant imported packages. In contrast, miller uses simple, easy-to-read code for each of the above requests:
```
name_functions(item)
name_properties(item)
name_fields(item)
```
In addition, each of those **miller** functions includes a boolean parameter `include_privates` which indicates whether you want to include any matching items that have str names beginning with an underscore.

## Intuitive

Unlike the default Python instrospection functions and methods, **miller** uses a consistent syntax and structure that is far more intuitive. This allows users to guess what the appropriate syntax should by following a simple, consistent structure.

**miller** uses five basic prefixes for its introspection functions:

| prefix   | what it does   | returns   |
|---|---|---|
| `catalog`  |combines results of corresponding  `name` and `get` functions into a `dict`  | `dict[str, Any]`   |
| `get`  | gets sought types from an item  |   `list[Any]`   |
| `has`  | whether an item has specified types  |   `bool`   |
| `is` | whether an item is a type  |   `bool`   |
| `name` | gets `str` names of sought types from an item  |   `list[str]`   |

Those prefixes are followed by an underscore and a suffix indicating what information is sought. **miller** has XXX possible suffixes for each of those prefixes:
| suffix  | what it concerns   | what types it inspects   |
|---|---|---|
| `annotations`  | class, function, or method annotations   | `object`, `Type`, or `ModuleType`  |
| `attribute`  | an attribute (including methods) of a class  | attribute in an `object` or `Type` |
| `attributes`  | attributes (including methods or functions)  |  `object`, `Type`, or `ModuleType`  |
| `class`  | a class (not an instance)  | `object` or `Type` |
| `classes`  | classes in a module    | `ModuleType`   |
| `field`  | field in a dataclass  | `dataclass` or `Type[dataclass]` |
| `fields`  | fields in a dataclass  | `dataclass` or `Type[dataclass]`  |
| `file_path`  | path of a file | `str` or `Path`  |
| `file_paths`  | paths of files in a path  | `str` or `Path`  |
| `folder_path`  | path of a folder  | `str` or `Path`  |
| `folder_paths`  | paths of folders in a path   | `str` or `Path`  |
| `function`  | a callable function  | `object`|
| `functions`  | functions in a module  | `ModuleType`  |
| `instance`  | a class instance (not a class)  | `object` or `Type` |
| `method`  | method in a class  | attribute in an `object` or `Type` |
| `methods`  | class or instance methods  | `object` or `Type`   |
| `module`  | module types  | `object` or `Type` |
| `modules`  | paths of modules in a path   |  `str` or `Path`  |
| `path`  | path on disk  | `str` or `Path` |
| `paths`  | combination of file_paths and folder_paths  | `str` or `Path`   |
| `property`  | attributes of a class  | attribute in an `object` |
| `properties`  | properties of a class  | `object` or `Type`   |
| `signatures`  | class, function, or method signatures  | `object`, `Type`, or `ModuleType`    |
| `variable`  | attributes (excluding methods) of a class | `object`, `Type`, or `ModuleType`   |
| `variables`  | an attribute (excluding methods or functions)  |  `object`, `Type`, or `ModuleType`   |

The following functions are available in **miller** for the `catalog`, `get`, `has`, and `name`  suffixes :

| prefix/suffix | `catalog`  | `get`  | `has`  | `name`  |
|---|---|---|---|---|---|---|
| `annotations` | X | X | X | X |
| `attributes` | X | X | X | X | 
| `classes` | X | X | X | X | 
| `fields` | X | X | X | X | 
| `file_paths` | X | X | X | X | 
| `folder_paths` | X | X | X | X | 
| `functions` | X | X | X | X | 
| `methods` | X | X | X | X | 
| `modules` | X | X | X | X |  
| `paths`  | X | X | X | X | 
| `properties` | X | X | X | X | 
| `signatures` | X | X | X | X | 
| `variables` | X | X | X | X | 

For the `is` prefix, functions with the following suffixes are included: 

 So, for example, 

* `catalog_methods`: returns a dict of the method names and methods of an object.
* `get_methods`: returns a list of methods of an object.
* `has_methods`: returns whether an object has all of the named methods passed to the `methods` parameter.
* `is_method`: returns whether an item is a method of an object.
* `name_methods`: returns a list of names of methods of an object.

# Contributing 

The project is highly documented so that users and developers can make **miller** work with their projects. It is designed for Python coders at all levels. Beginners should be able to follow the readable code and internal documentation to understand how it works. More advanced users should find complex and tricky problems addressed through efficient code.
