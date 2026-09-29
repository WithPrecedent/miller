"""General-purpose helper functions used throughout miller.

Contents:
    iterify: wraps non-iterable items in a list.
    namify: returns a str name for any item.
    pathlibify: converts a str or path-like object to a `pathlib.Path`.
    is_private_name: whether a str name begins with an underscore.
    drop_privates: removes private names from a list or dict.

"""

from __future__ import annotations

import os
import pathlib
from collections.abc import Iterable, Mapping
from typing import Any, TypeVar

_T = TypeVar("_T")


def iterify(item: Any) -> Iterable[Any]:
    """Returns `item` if it is iterable or otherwise wraps it in a list.

    `str` and `bytes` objects are treated as single items rather than as
    iterables of characters or integers. `None` becomes an empty list.

    Args:
        item: object to make iterable.

    Returns:
        `item` if it was already iterable (and not `str` or `bytes`), an empty
            list if `item` is None, or a list containing `item` otherwise.

    """
    if item is None:
        return []
    if isinstance(item, (str, bytes, bytearray)):
        return [item]
    if isinstance(item, Iterable):
        return item
    return [item]


def namify(item: Any, default: str | None = None) -> str:
    """Returns a str name for `item`.

    The name is found, in order of preference, from: `item` itself (if it is a
    `str`), a str `name` attribute, a str `__name__` attribute, `default` (if
    passed), and, finally, the name of the class of `item`.

    Args:
        item: object to name.
        default: name to return if no name can be found on `item`. Defaults to
            None, which means the name of the class of `item` is used.

    Returns:
        A str name for `item`.

    """
    if isinstance(item, str):
        return item
    for attribute in ("name", "__name__"):
        try:
            name = getattr(item, attribute)
        except Exception:  # noqa: BLE001, S112
            continue
        if isinstance(name, str):
            return name
    if default is not None:
        return default
    return str(item.__class__.__name__)


def pathlibify(item: str | os.PathLike[str]) -> pathlib.Path:
    """Returns `item` as a `pathlib.Path`.

    Args:
        item: str or path-like object.

    Raises:
        TypeError: if `item` cannot be converted to a path.

    Returns:
        `item` as a `pathlib.Path`.

    """
    if isinstance(item, pathlib.Path):
        return item
    if isinstance(item, (str, os.PathLike)):
        return pathlib.Path(item)
    message = f"item must be a str or path-like object, not {type(item)}"
    raise TypeError(message)


def is_private_name(name: str) -> bool:
    """Returns whether `name` begins with an underscore.

    Args:
        name: str name to examine.

    Returns:
        Whether `name` is a "private" (or "dunder") name.

    """
    return name.startswith("_")


def drop_privates(item: _T) -> _T:
    """Returns `item` without any str names that begin with an underscore.

    Args:
        item: list (or other iterable) of str names or a mapping with str
            keys. Lists and mappings are returned as new objects of the same
            general type (`list` for iterables, `dict` for mappings).

    Returns:
        A new list or dict with private names removed.

    """
    if isinstance(item, Mapping):
        return {  # type: ignore[return-value]
            k: v
            for k, v in item.items()
            if not (isinstance(k, str) and is_private_name(k))
        }
    return [  # type: ignore[return-value]
        i
        for i in item  # type: ignore[attr-defined]
        if not (isinstance(i, str) and is_private_name(i))
    ]
