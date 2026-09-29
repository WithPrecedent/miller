"""Introspection of the classes and functions defined in python modules.

Only objects defined in a module are included. Objects that the module simply
imported from elsewhere are ignored.

Contents:
    catalog_classes, collect_classes, has_classes, name_classes
    catalog_functions, collect_functions, has_functions, name_functions

"""

from __future__ import annotations

import importlib
import inspect
import types
from collections.abc import Callable
from typing import Any

from . import base

__all__: list[str] = [
    'catalog_classes',
    'catalog_functions',
    'collect_classes',
    'collect_functions',
    'has_classes',
    'has_functions',
    'name_classes',
    'name_functions']


def _modulify(item: types.ModuleType | str) -> types.ModuleType:
    """Returns `item` as a module, importing it if it is a str name."""
    if isinstance(item, types.ModuleType):
        return item
    if isinstance(item, str):
        return importlib.import_module(item)
    message = f'item must be a module or module name, not {type(item)}'
    raise TypeError(message)


def _members(
    item: types.ModuleType | str,
    predicate: Callable[[Any], bool],
    include_privates: bool | None) -> dict[str, Any]:
    """Returns members of module `item` that are defined in that module."""
    module = _modulify(item)
    members = {
        n: o for n, o in inspect.getmembers(module, predicate)
        if getattr(o, '__module__', None) == module.__name__}
    return base.catalog_where(
        names = members,
        predicate = lambda _: True,
        getter = members.__getitem__,
        include_privates = include_privates)


def name_classes(
    item: types.ModuleType | str,
    include_privates: bool | None = None) -> list[str]:
    """Returns names of the classes defined in module `item`.

    Args:
        item: module or importable module name to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of class names.

    """
    return list(catalog_classes(item, include_privates))


def collect_classes(
    item: types.ModuleType | str,
    include_privates: bool | None = None) -> list[type]:
    """Returns the classes defined in module `item`.

    Args:
        item: module or importable module name to examine.
        include_privates: whether to include classes whose names begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of classes.

    """
    return list(catalog_classes(item, include_privates).values())


def catalog_classes(
    item: types.ModuleType | str,
    include_privates: bool | None = None) -> dict[str, type]:
    """Returns a dict of the names and classes defined in module `item`.

    Args:
        item: module or importable module name to examine.
        include_privates: whether to include classes whose names begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        Dict of class names and classes.

    """
    return _members(item, inspect.isclass, include_privates)


def has_classes(
    item: types.ModuleType | str,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None) -> bool:
    """Returns whether `names` are classes defined in module `item`.

    Args:
        item: module or importable module name to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `names` are classes defined in `item`.

    """
    classes = _members(item, inspect.isclass, include_privates = True)
    return base.has_names(
        item, names, base.membership(classes), raise_error, match_all)


def name_functions(
    item: types.ModuleType | str,
    include_privates: bool | None = None) -> list[str]:
    """Returns names of the functions defined in module `item`.

    Args:
        item: module or importable module name to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of function names.

    """
    return list(catalog_functions(item, include_privates))


def collect_functions(
    item: types.ModuleType | str,
    include_privates: bool | None = None) -> list[types.FunctionType]:
    """Returns the functions defined in module `item`.

    Args:
        item: module or importable module name to examine.
        include_privates: whether to include functions whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of functions.

    """
    return list(catalog_functions(item, include_privates).values())


def catalog_functions(
    item: types.ModuleType | str,
    include_privates: bool | None = None) -> dict[str, types.FunctionType]:
    """Returns a dict of the names and functions defined in module `item`.

    Args:
        item: module or importable module name to examine.
        include_privates: whether to include functions whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        Dict of function names and functions.

    """
    return _members(item, inspect.isfunction, include_privates)


def has_functions(
    item: types.ModuleType | str,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None) -> bool:
    """Returns whether `names` are functions defined in module `item`.

    Args:
        item: module or importable module name to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `names` are functions defined in `item`.

    """
    functions = _members(item, inspect.isfunction, include_privates = True)
    return base.has_names(
        item, names, base.membership(functions), raise_error, match_all)
