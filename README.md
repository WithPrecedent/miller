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
[m[0] for m in inspect.getmembers(item, inspect.isfunction) 
 if m[1].__module__ == item.__name__]

"""Returns names of properties of the instance 'item'."""
[a for a in dir(item) if isinstance(getattr(a, item), property)] 

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
| `map`  |combines results of corresponding  `name` and `get` functions into a `dict`  | `dict[str, Any]`   |
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
| `class_attribute`  | attributes of a class (not an instance)  | `object` or `Type` |
| `class_attributes`  | attributes of a class (not an instance)    | `object` or `Type`    |
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

The following functions are available in **miller** for the `map`, `get`, `has`, and `name`  suffixes :

| prefix/suffix | `map`  | `get`  | `has`  | `name`  |
|---|---|---|---|---|
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

* `map_methods`: returns a dict of the method names and methods of an object.
* `list_methods`: returns a list of methods of an object.
* `has_methods`: returns whether an object has all of the named methods passed to the `methods` parameter.
* `is_method`: returns whether an item is a method of an object.
* `name_methods`: returns a list of names of methods of an object.

<p align="center">
<img src="https://media.giphy.com/media/l0Ex6Yb0meOZQloWs/giphy.gif" height="300"/>
</p>


## Getting started

*“Go into a room too fast, kid… The room eats you.”*  - Detective Josephus
Miller


### Requirements

[TODO: List any OS or other restrictions and pre-installation dependencies]

### Installation

To install `miller`, use `pip`:

```sh
pip install miller
```

### Usage

[TODO: Describe common use cases, with possible example(s)]

## Contributing

Contributors are always welcome. Feel free to grab an [issue](https://www.github.com/WithPrecedent/miller/issues) to work on or make a suggested improvement. If you wish to contribute, please read the [Contribution Guide](https://www.github.com/WithPrecedent/miller/contributing.md) and [Code of Conduct](https://www.github.com/WithPrecedent/miller/code_of_conduct.md).

## Similar Projects

[TODO: If they exist, it is always nice to acknowledge other similar efforts]

## Acknowledgments

[TODO: Mention any people or organizations that warrant a special acknowledgment]

## License

Use of this repository is authorized under the [Apache Software License 2.0](https://www.github.com/WithPrecedent/miller/blog/main/LICENSE).
