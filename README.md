[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PyPI Latest Release](https://img.shields.io/pypi/v/miller.svg)](https://pypi.org/project/miller/) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Documentation Status](https://readthedocs.org/projects/miller/badge/?version=latest)](http://miller.readthedocs.io/?badge=latest)

# What is miller?

*"I'm a tool that finds things."* - Detective Josephus Miller

Named after the erstwhile inspector from *The Expanse*, this package provides convenient, simple introspection tools for packages, modules, classes, objects, attributes, and containers. 

# Why miller?

## Simple

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

**miller** uses four basic prefixes for its core introspection functions:
 
* `get`: returns the items sought.
* `has`: returns a bool as to whether a class or object has a list of items.
* `is`: returns a bool as to whether a class or object is a type.
* `name`: returns the str names of the items sought.
  
Those prefixes are followed by an underscore and a suffix indicating what information is sought. So, for example, 

* `get_methods`: returns a dict of the method names and methods of an object.
* `has_methods`: returns whether an object has all of the named methods passed to the `methods` parameter.
* `is_method`: returns whether an item is a method of an object.
* `name_methods`: returns a list of names of methods of an object.

# Contributing 

The project is highly documented so that users and developers can make **miller** work with their projects. It is designed for Python coders at all levels. Beginners should be able to follow the readable code and internal documentation to understand how it works. More advanced users should find complex and tricky problems addressed through efficient code.
