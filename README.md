# miller

| | |
| --- | --- |
| Version | [![PyPI Latest Release](https://img.shields.io/pypi/v/miller.svg?style=for-the-badge&color=steelblue&label=PyPI&logo=PyPI&logoColor=yellow)](https://pypi.org/project/miller/) [![GitHub Latest Release](https://img.shields.io/github/v/tag/WithPrecedent/miller?style=for-the-badge&color=navy&label=GitHub&logo=github)](https://github.com/WithPrecedent/miller/releases)
| Status | [![Build Status](https://img.shields.io/github/actions/workflow/status/WithPrecedent/miller/ci.yml?branch=main&style=for-the-badge&color=cadetblue&label=Tests&logo=pytest)](https://github.com/WithPrecedent/miller/actions/workflows/ci.yml?query=branch%3Amain) [![Development Status](https://img.shields.io/badge/Development-Active-seagreen?style=for-the-badge&logo=git)](https://www.repostatus.org/#active) [![Project Stability](https://img.shields.io/pypi/status/miller?style=for-the-badge&logo=pypi&label=Stability&logoColor=yellow)](https://pypi.org/project/miller/)
| Documentation | [![Hosted By](https://img.shields.io/badge/Hosted_by-Github_Pages-blue?style=for-the-badge&color=navy&logo=github)](https://WithPrecedent.github.io/miller)
| Tools | [![Documentation](https://img.shields.io/badge/MkDocs-magenta?style=for-the-badge&color=deepskyblue&logo=markdown&labelColor=gray)](https://squidfunk.github.io/mkdocs-material/) [![Linter](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/charliermarsh/Ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/Ruff) [![Dependency Manager](https://img.shields.io/badge/PDM-mediumpurple?style=for-the-badge&logo=affinity&labelColor=gray)](https://PDM.fming.dev) [![Pre-commit](https://img.shields.io/badge/pre--commit-darkolivegreen?style=for-the-badge&logo=pre-commit&logoColor=white&labelColor=gray)](https://github.com/TezRomacH/python-package-template/blob/master/.pre-commit-config.yaml) [![CI](https://img.shields.io/badge/GitHub_Actions-navy?style=for-the-badge&logo=githubactions&labelColor=gray&logoColor=white)](https://github.com/features/actions) [![Editor Settings](https://img.shields.io/badge/Editor_Config-paleturquoise?style=for-the-badge&logo=editorconfig&labelColor=gray)](https://editorconfig.org/) [![Repository Template](https://img.shields.io/badge/snickerdoodle-bisque?style=for-the-badge&logo=cookiecutter&labelColor=gray)](https://www.github.com/WithPrecedent/miller) [![Dependency Maintainer](https://img.shields.io/badge/dependabot-navy?style=for-the-badge&logo=dependabot&logoColor=white&labelColor=gray)](https://github.com/dependabot)
| Compatibility | [![Compatible Python Versions](https://img.shields.io/pypi/pyversions/miller?style=for-the-badge&color=steelblue&label=Python&logo=python&logoColor=yellow)](https://pypi.python.org/pypi/miller/) [![Linux](https://img.shields.io/badge/Linux-lightseagreen?style=for-the-badge&logo=linux&labelColor=gray&logoColor=white)](https://www.linux.org/) [![MacOS](https://img.shields.io/badge/MacOS-snow?style=for-the-badge&logo=apple&labelColor=gray)](https://www.apple.com/macos/) [![Windows](https://img.shields.io/badge/windows-blue?style=for-the-badge&logo=Windows&labelColor=gray&color=orangered)](https://www.microsoft.com/en-us/windows?r=1)
| Stats | [![PyPI Download Rate (per month)](https://img.shields.io/pypi/dm/miller?style=for-the-badge&color=steelblue&label=Downloads%20💾&logo=pypi&logoColor=yellow)](https://pypi.org/project/miller) [![GitHub Stars](https://img.shields.io/github/stars/WithPrecedent/miller?style=for-the-badge&color=navy&label=Stars%20⭐&logo=github)](https://github.com/WithPrecedent/miller/stargazers) [![GitHub Contributors](https://img.shields.io/github/contributors/WithPrecedent/miller?style=for-the-badge&color=navy&label=Contributors%20🙋&logo=github)](https://github.com/WithPrecedent/miller/graphs/contributors) [![GitHub Issues](https://img.shields.io/github/issues/WithPrecedent/miller?style=for-the-badge&color=navy&label=Issues%20📘&logo=github)](https://github.com/WithPrecedent/miller/graphs/contributors) [![GitHub Forks](https://img.shields.io/github/forks/WithPrecedent/miller?style=for-the-badge&color=navy&label=Forks%20🍴&logo=github)](https://github.com/WithPrecedent/miller/forks)
| | |

-----

## What is miller?

*This package is under heavy construction. Use at your own risk*

*"I'm a tool that finds things."* - Detective Josephus Miller

<p align="center">
<img src="https://media.giphy.com/media/l44Q6pEdnMOQqHgek/giphy.gif" height="300"/>
</p>

Named after the erstwhile inspector from *The Expanse*, this package provides convenient, introspection tools using a consistent, intuitive syntax for packages, modules, classes, objects, attributes, and containers.

## Why use miller?

### Universal

Consider the different and often difficult-to-read syntax that Python uses for
introspection of different objects.

``` python
"""Returns a list of function names in the module 'item'."""

[
    m[0]
    for m in inspect.getmembers(item, inspect.isfunction)
    if m[1].__module__ == item.__name__
]

"""Returns names of properties of the instance 'item'."""
[a for a in dir(type(item)) if isinstance(getattr(type(item), a), property)]

"""Returns names of fields of the dataclass 'item'."""
[f.name for f in dataclasses.fields(item)]
```

That code can be difficult to remember, requires importing a range of packages, and is not easy to understand if you are not familiar with the relevant imported packages.

<p align="center">
<img src="https://media.giphy.com/media/3oz8xxBsDMZWcMCHoQ/giphy.gif" height="300"/>
</p>

In contrast, **miller** uses simple, easy-to-read code for each of the above requests:

``` python
name_functions(item)
name_properties(item)
name_fields(item)
```

In addition, each of those **miller** functions includes a boolean parameter `include_privates` which indicates whether you want to include any matching items that have str names beginning with an underscore.

### Intuitive

<p align="center">
<img src="https://media.giphy.com/media/PiqvXUF6UI6enzyNY9/giphy.gif" height="300"/>
</p>

Unlike the default Python instrospection functions and methods, **miller** uses a consistent syntax and structure that is far more intuitive. This allows users to guess what the appropriate syntax should by following a simple, consistent structure.

**miller** uses five basic prefixes for its introspection functions:

| prefix   | what it does   | returns   |
|---|---|---|
| `catalog`  |combines results of corresponding  `name` and `collect` functions into a `dict`  | `dict[str, Any]`   |
| `collect`  | gets sought kinds from an item  |   `list[Any]`   |
| `has`  | whether an item has specific attributes of a kind |   `bool`   |
| `is` | whether an item is a particular kind  |   `bool`   |
| `name` | gets `str` names of sought kinds from an item  |   `list[str]`   |

Those prefixes are followed by an underscore and a suffix indicating what information is sought. **miller** has 28 possible suffixes (not every suffix is available for every prefix):

| suffix  | what it concerns   | what types it inspects   |
|---|---|---|
| `annotations`  | type annotations of a class, function, or module   | `object`, `Type`, `ModuleType`, or function  |
| `attribute`  | an attribute (including methods) of an item  | attribute in an `object`, `Type`, or `ModuleType` |
| `attributes`  | attributes (including methods or functions)  |  `object`, `Type`, or `ModuleType`  |
| `class`  | a class (not an instance)  | `object` or `Type` |
| `classes`  | classes in a module    | `ModuleType`   |
| `class_attribute`  | an attribute defined on a class (not an instance)  | `object` or `Type` |
| `class_attributes`  | attributes defined on a class (not an instance)    | `object` or `Type`    |
| `field`  | field in a dataclass  | `dataclass` or `Type[dataclass]` |
| `fields`  | fields in a dataclass  | `dataclass` or `Type[dataclass]`  |
| `file_path`  | path of a file | `str` or `Path`  |
| `file_paths`  | paths of files in a path  | `str` or `Path`  |
| `folder_path`  | path of a folder  | `str` or `Path`  |
| `folder_paths`  | paths of folders in a path   | `str` or `Path`  |
| `function`  | a callable function  | `object`|
| `functions`  | functions in a module  | `ModuleType`  |
| `instance`  | a class instance (not a class)  | `object` |
| `instance_attributes`  | attributes stored on an instance  | `object` |
| `method`  | method (or function) of an item  | attribute in an `object`, `Type`, or `ModuleType` |
| `methods`  | class or instance methods  | `object` or `Type`   |
| `module`  | a module or the path to a python module  | `ModuleType`, `str`, or `Path` |
| `modules`  | python modules in a folder   |  `str` or `Path`  |
| `path`  | path to something that exists on disk  | `str` or `Path` |
| `paths`  | combination of file_paths and folder_paths in a folder  | `str` or `Path`   |
| `property`  | a property of a class  | attribute in an `object` or `Type` |
| `properties`  | properties of a class  | `object` or `Type`   |
| `signatures`  | signatures of methods (or functions in a module)  | `object`, `Type`, or `ModuleType`    |
| `variable`  | an attribute (excluding methods or properties) | `object`, `Type`, or `ModuleType`   |
| `variables`  | attributes (excluding methods or properties)  |  `object`, `Type`, or `ModuleType`   |

The following functions are available in **miller** for the `catalog`, `collect`, `has`, and `name` prefixes:

| suffix/prefix | `catalog`  | `collect`  | `has`  | `name`  |
|---|---|---|---|---|
| `annotations` | X | X | X | X |
| `attributes` | X | X | X | X |
| `classes` | X | X | X | X |
| `class_attributes` | X | X | X | X |
| `fields` | X | X | X | X |
| `file_paths` | X | X | X | X |
| `folder_paths` | X | X | X | X |
| `functions` | X | X | X | X |
| `instance_attributes` | X | X | X | X |
| `methods` | X | X | X | X |
| `modules` | X | X | X | X |
| `paths`  | X | X | X | X |
| `properties` | X | X | X | X |
| `signatures` | X | X | X | X |
| `variables` | X | X | X | X |

The `is` prefix has functions for the following singular suffixes: `attribute`, `class`, `class_attribute`, `field`, `file_path`, `folder_path`, `function`, `instance`, `method`, `module`, `path`, `property`, and `variable`. It also includes `is_container`, `is_dict`, `is_dunder`, `is_iterable`, `is_list`, `is_nested`, `is_object`, `is_private`, `is_sequence`, `is_set`, and `is_tuple`. `is_file` and `is_folder` are short aliases of `is_file_path` and `is_folder_path`.

So, for example,

* `catalog_methods`: returns a dict of the method names and methods of an object.
* `collect_methods`: returns a list of methods of an object.
* `has_methods`: returns whether an object has all (or, if `match_all = False`, any) of the named methods passed to the `names` parameter.
* `is_method`: returns whether an item is a method of an object.
* `name_methods`: returns a list of names of methods of an object.

<p align="center">
<img src="https://media.giphy.com/media/l0Ex6Yb0meOZQloWs/giphy.gif" height="300"/>
</p>


## Getting started

*“Go into a room too fast, kid… The room eats you.”*  - Detective Josephus
Miller


### Requirements

**miller** requires Python 3.10 or later and has no other dependencies. It runs on Linux, MacOS, and Windows.

### Installation

To install `miller`, use `pip`:

```sh
pip install miller
```

### Usage

``` python
import dataclasses

import miller


@dataclasses.dataclass
class Example:
    one: int = 1
    _two: int = 2

    def add(self, other: int) -> int:
        return self.one + other

    @property
    def double(self) -> int:
        return self.one * 2


item = Example()

miller.name_methods(item)  # ['add']
miller.name_properties(item)  # ['double']
miller.name_fields(item)  # ['one']
miller.name_fields(item, include_privates=True)  # ['one', '_two']
miller.catalog_variables(item)  # {'one': 1}
miller.has_methods(item, "add")  # True
miller.is_property(item, "double")  # True
miller.name_functions(miller.framework)  # functions defined in a module
miller.name_modules("src/miller")  # python modules in a folder
```

Functions that check whether an item qualifies (`has_*` and `is_*`) return `False` by default. Pass `raise_error = True` (or call `miller.set_raise_errors(True)`) to have them raise an error instead. The `miller.set_*` functions change the global defaults for `include_privates`, `include_str`, `match_all`, `raise_errors`, `recursive`, module file suffixes, and the function used to name items.

**miller** also provides `Inspector`, which returns an object-oriented inspector appropriate to whatever is passed to it (a module, a folder, a class, or an instance):

``` python
inspector = miller.Inspector(item)
inspector.methods  # {'add': <bound method Example.add ...>}
inspector.variables  # {'one': 1}
inspector.fields  # {'one': Field(...)}
```

## Contributing

Contributors are always welcome. Feel free to grab an [issue](https://www.github.com/WithPrecedent/miller/issues) to work on or make a suggested improvement. If you wish to contribute, please read the [Contribution Guide](https://www.github.com/WithPrecedent/miller/contributing.md) and [Code of Conduct](https://www.github.com/WithPrecedent/miller/code_of_conduct.md).

## Similar Projects

The standard library's [`inspect`](https://docs.python.org/3/library/inspect.html) module offers the underlying tools that **miller** wraps in a more consistent syntax.

## Acknowledgments

This project was generated from [@WithPrecedent](https://github.com/WithPrecedent)'s [![cookiecutter Template](https://img.shields.io/badge/snickerdoodle-bisque?style=for-the-badge&logo=cookiecutter&labelColor=gray)](https://www.github.com/WithPrecedent/snickerdoodle) template.

## License

Use of this repository is authorized under the [Apache Software License 2.0](https://www.github.com/WithPrecedent/miller/blob/main/LICENSE).
