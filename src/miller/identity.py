"""Functions that identify what kind of thing an item is.

Contents:
    is_class: whether an item is a class (and not an instance).
    is_container: whether an item is a container.
    is_dict: whether an item is a dict or other mutable mapping.
    is_dunder: whether an item has a name like `__name__`.
    is_file: whether an item is a path to an existing file.
    is_file_path: same as `is_file`.
    is_folder: whether an item is a path to an existing folder.
    is_folder_path: same as `is_folder`.
    is_function: whether an item is a function.
    is_instance: whether an item is an instance (and not a class).
    is_iterable: whether an item is iterable.
    is_list: whether an item is a list or other mutable sequence.
    is_module: whether an item is a module or a path to a python module.
    is_nested: whether an item contains other containers.
    is_nested_dict: whether an item is a mapping containing other containers.
    is_nested_list: whether an item is a list containing other containers.
    is_nested_set: whether an item is a set containing other containers.
    is_nested_tuple: whether an item is a tuple containing other containers.
    is_object: whether an item is an object (not a class, function, or module).
    is_path: whether an item is a path to something that exists.
    is_private: whether an item has a name beginning with an underscore.
    is_sequence: whether an item is a sequence.
    is_set: whether an item is a set.
    is_tuple: whether an item is a tuple.

"""

from __future__ import annotations

import inspect
import os
import pathlib
import types
from collections.abc import (
    Container,
    Iterable,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
)
from collections.abc import Set as AbstractSet
from typing import Any

from . import base, configuration, utilities

__all__: list[str] = [
    "is_class",
    "is_container",
    "is_dict",
    "is_dunder",
    "is_file",
    "is_file_path",
    "is_folder",
    "is_folder_path",
    "is_function",
    "is_instance",
    "is_iterable",
    "is_list",
    "is_module",
    "is_nested",
    "is_nested_dict",
    "is_nested_list",
    "is_nested_set",
    "is_nested_tuple",
    "is_object",
    "is_path",
    "is_private",
    "is_sequence",
    "is_set",
    "is_tuple",
]

_STR_LIKE: tuple[type, ...] = (str, bytes, bytearray)
_MIN_DUNDER_LENGTH: int = 4


def _kind_of(item: Any) -> type:
    """Returns `item` if it is a class or otherwise the class of `item`."""
    return item if inspect.isclass(item) else item.__class__


def _is_type(
    item: Any, kind: type | tuple[type, ...], include_str: bool | None = None
) -> bool:
    """Returns whether `item` (or its class) is a subclass of `kind`."""
    include_str = base.resolve(include_str, configuration.INCLUDE_STR)
    cls = _kind_of(item)
    return issubclass(cls, kind) and (
        include_str or not issubclass(cls, _STR_LIKE)
    )


def is_class(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` is a class (and not an instance).

    Args:
        item: object to examine.
        raise_error: whether to raise a `TypeError` if `item` is not a class.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a class.

    """
    return base.verdict(
        inspect.isclass(item), raise_error, f"{item!r} is not a class"
    )


def is_container(
    item: Any, include_str: bool | None = None, raise_error: bool | None = None
) -> bool:
    """Returns whether `item` is a container.

    Args:
        item: class or instance to examine.
        include_str: whether `str` and `bytes` count as containers. If None,
            `miller.configuration.INCLUDE_STR` is used.
        raise_error: whether to raise a `TypeError` if `item` is not a
            container. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a container.

    """
    return base.verdict(
        _is_type(item, Container, include_str),
        raise_error,
        f"{item!r} is not a container",
    )


def is_dict(
    item: Any, *, include_generic: bool = True, raise_error: bool | None = None
) -> bool:
    """Returns whether `item` is a dict or other mutable mapping.

    Args:
        item: class or instance to examine.
        include_generic: whether any `MutableMapping` counts (True) or only
            actual `dict` types (False). Defaults to True.
        raise_error: whether to raise a `TypeError` if `item` is not a dict.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a dict (or, if `include_generic`, a mutable mapping).

    """
    kind = MutableMapping if include_generic else dict
    return base.verdict(
        issubclass(_kind_of(item), kind), raise_error, f"{item!r} is not a dict"
    )


def is_dunder(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` has a name like `__name__`.

    Args:
        item: str name or object with a name to examine.
        raise_error: whether to raise a `TypeError` if the name is not a dunder
            name. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether the name of `item` begins and ends with two underscores.

    """
    name = configuration.KEYER(item)
    return base.verdict(
        len(name) > _MIN_DUNDER_LENGTH
        and name.startswith("__")
        and name.endswith("__"),
        raise_error,
        f"{name} is not a dunder name",
    )


def is_file_path(
    item: str | os.PathLike[str], raise_error: bool | None = None
) -> bool:
    """Returns whether `item` is a path to an existing file.

    Args:
        item: path to check.
        raise_error: whether to raise a `TypeError` if `item` is not a file. If
            None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a path to an existing file.

    """
    return base.verdict(
        _path_or_none(item, lambda p: p.is_file()),
        raise_error,
        f"{item!r} is not a path to a file",
    )


def is_folder_path(
    item: str | os.PathLike[str], raise_error: bool | None = None
) -> bool:
    """Returns whether `item` is a path to an existing folder.

    Args:
        item: path to check.
        raise_error: whether to raise a `TypeError` if `item` is not a folder.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a path to an existing folder.

    """
    return base.verdict(
        _path_or_none(item, lambda p: p.is_dir()),
        raise_error,
        f"{item!r} is not a path to a folder",
    )


def is_function(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` is a function.

    Args:
        item: object to examine.
        raise_error: whether to raise a `TypeError` if `item` is not a
            function. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a function.

    """
    return base.verdict(
        isinstance(item, types.FunctionType),
        raise_error,
        f"{item!r} is not a function",
    )


def is_instance(
    item: Any,
    kind: type | tuple[type, ...] | None = None,
    raise_error: bool | None = None,
) -> bool:
    """Returns whether `item` is an instance (and not a class).

    Args:
        item: object to examine.
        kind: optional class (or tuple of classes) that `item` must be an
            instance of. Defaults to None.
        raise_error: whether to raise a `TypeError` if `item` is not an
            instance. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is an instance (of `kind`, if passed).

    """
    value = not inspect.isclass(item)
    if kind is not None:
        value = value and isinstance(item, kind)
    return base.verdict(value, raise_error, f"{item!r} is not an instance")


def is_iterable(
    item: Any, include_str: bool | None = None, raise_error: bool | None = None
) -> bool:
    """Returns whether `item` is iterable.

    Args:
        item: class or instance to examine.
        include_str: whether `str` and `bytes` count as iterable. If None,
            `miller.configuration.INCLUDE_STR` is used.
        raise_error: whether to raise a `TypeError` if `item` is not iterable.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is iterable.

    """
    return base.verdict(
        _is_type(item, Iterable, include_str),
        raise_error,
        f"{item!r} is not iterable",
    )


def is_list(
    item: Any, *, include_generic: bool = True, raise_error: bool | None = None
) -> bool:
    """Returns whether `item` is a list or other mutable sequence.

    Args:
        item: class or instance to examine.
        include_generic: whether any `MutableSequence` counts (True) or only
            actual `list` types (False). Defaults to True.
        raise_error: whether to raise a `TypeError` if `item` is not a list. If
            None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a list (or, if `include_generic`, a mutable
            sequence).

    """
    kind = MutableSequence if include_generic else list
    return base.verdict(
        issubclass(_kind_of(item), kind), raise_error, f"{item!r} is not a list"
    )


def is_module(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` is a module or a path to a python module file.

    Args:
        item: module, str, or path-like object to examine.
        raise_error: whether to raise a `TypeError` if `item` is not a module.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a module or a path to an existing file with one of
            the suffixes in `miller.configuration.MODULE_EXTENSIONS`.

    """
    if isinstance(item, types.ModuleType):
        value = True
    else:
        value = _path_or_none(
            item,
            lambda p: (
                p.is_file() and p.suffix in configuration.MODULE_EXTENSIONS
            ),
        )
    return base.verdict(value, raise_error, f"{item!r} is not a module")


def is_object(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` is an object (not a class, function, or module).

    Args:
        item: object to examine.
        raise_error: whether to raise a `TypeError` if `item` is not an
            object. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is an object.

    """
    value = not (
        inspect.isclass(item)
        or inspect.isroutine(item)
        or inspect.ismodule(item)
    )
    return base.verdict(value, raise_error, f"{item!r} is not an object")


def is_path(
    item: str | os.PathLike[str], raise_error: bool | None = None
) -> bool:
    """Returns whether `item` is a path to something that exists.

    Args:
        item: path to check.
        raise_error: whether to raise a `TypeError` if `item` is not an
            existing path. If None, `miller.configuration.RAISE_ERRORS` is
            used.

    Returns:
        Whether `item` is an existing path.

    """
    return base.verdict(
        _path_or_none(item, lambda p: p.exists()),
        raise_error,
        f"{item!r} is not an existing path",
    )


def is_private(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` has a name beginning with an underscore.

    Args:
        item: str name or object with a name to examine.
        raise_error: whether to raise a `TypeError` if the name is not private.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether the name of `item` begins with an underscore.

    """
    name = configuration.KEYER(item)
    return base.verdict(
        utilities.is_private_name(name),
        raise_error,
        f"{name} is not a private name",
    )


def is_sequence(
    item: Any, include_str: bool | None = None, raise_error: bool | None = None
) -> bool:
    """Returns whether `item` is a sequence.

    Args:
        item: class or instance to examine.
        include_str: whether `str` and `bytes` count as sequences. If None,
            `miller.configuration.INCLUDE_STR` is used.
        raise_error: whether to raise a `TypeError` if `item` is not a
            sequence. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a sequence.

    """
    return base.verdict(
        _is_type(item, Sequence, include_str),
        raise_error,
        f"{item!r} is not a sequence",
    )


def is_set(
    item: Any, *, include_generic: bool = True, raise_error: bool | None = None
) -> bool:
    """Returns whether `item` is a set (or `frozenset`) or other set type.

    Args:
        item: class or instance to examine.
        include_generic: whether any `collections.abc.Set` counts (True) or
            only actual `set` and `frozenset` types (False). Defaults to True.
        raise_error: whether to raise a `TypeError` if `item` is not a set. If
            None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a set.

    """
    kind = AbstractSet if include_generic else (set, frozenset)
    return base.verdict(
        issubclass(_kind_of(item), kind), raise_error, f"{item!r} is not a set"
    )


def is_tuple(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` is a tuple.

    Args:
        item: class or instance to examine.
        raise_error: whether to raise a `TypeError` if `item` is not a tuple.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a tuple.

    """
    return base.verdict(
        issubclass(_kind_of(item), tuple),
        raise_error,
        f"{item!r} is not a tuple",
    )


def _is_nested_container(item: Any) -> bool:
    """Returns whether `item` is a non-str container."""
    return not isinstance(item, _STR_LIKE) and isinstance(
        item, (Mapping, Sequence, AbstractSet)
    )


def is_nested(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` contains at least one other container.

    For mappings, the values are examined. For other containers, the elements
    are. `str` and `bytes` do not count as containers here.

    Args:
        item: instance to examine.
        raise_error: whether to raise a `TypeError` if `item` is not nested.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a container that holds at least one container.

    """
    if isinstance(item, Mapping):
        value = any(_is_nested_container(v) for v in item.values())
    elif _is_nested_container(item):
        value = any(_is_nested_container(i) for i in item)
    else:
        value = False
    return base.verdict(value, raise_error, f"{item!r} is not nested")


def is_nested_dict(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` is a mapping that contains another container.

    Args:
        item: instance to examine.
        raise_error: whether to raise a `TypeError` if `item` does not qualify.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a nested mapping.

    """
    value = isinstance(item, Mapping) and is_nested(item)
    return base.verdict(value, raise_error, f"{item!r} is not a nested dict")


def is_nested_list(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` is a list that contains another container.

    Args:
        item: instance to examine.
        raise_error: whether to raise a `TypeError` if `item` does not qualify.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a nested list.

    """
    value = isinstance(item, MutableSequence) and is_nested(item)
    return base.verdict(value, raise_error, f"{item!r} is not a nested list")


def is_nested_set(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` is a set that contains another container.

    Because most containers are not hashable, only sets containing
    `frozenset` or `tuple` objects will qualify.

    Args:
        item: instance to examine.
        raise_error: whether to raise a `TypeError` if `item` does not qualify.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a nested set.

    """
    value = isinstance(item, (MutableSet, frozenset)) and is_nested(item)
    return base.verdict(value, raise_error, f"{item!r} is not a nested set")


def is_nested_tuple(item: Any, raise_error: bool | None = None) -> bool:
    """Returns whether `item` is a tuple that contains another container.

    Args:
        item: instance to examine.
        raise_error: whether to raise a `TypeError` if `item` does not qualify.
            If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `item` is a nested tuple.

    """
    value = isinstance(item, tuple) and is_nested(item)
    return base.verdict(value, raise_error, f"{item!r} is not a nested tuple")


def _path_or_none(item: Any, check: Any) -> bool:
    """Returns whether `check` passes for `item` converted to a path."""
    if not isinstance(item, (str, os.PathLike)):
        return False
    try:
        return bool(check(pathlib.Path(item)))
    except (OSError, ValueError):
        return False


is_file = is_file_path
is_folder = is_folder_path
