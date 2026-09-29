"""Introspection of the contents of containers.

Contents:
    collect_types: returns the types of the items in a container.
    collect_key_types: returns the types of the keys in a mapping.
    has_types: returns whether a container holds items of specified types.

"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from . import base, utilities

__all__: list[str] = ["collect_key_types", "collect_types", "has_types"]


def _unique_types(items: Iterable[Any]) -> tuple[type, ...]:
    """Returns the distinct types of `items` in order of first appearance."""
    return tuple(dict.fromkeys(type(i) for i in items))


def collect_types(item: Any) -> tuple[type, ...]:
    """Returns the distinct types of the items in the container `item`.

    For mappings, the types of the values (not the keys) are returned. Use
    `collect_key_types` for the types of keys.

    Args:
        item: container to examine.

    Raises:
        TypeError: if `item` is not a container.

    Returns:
        Tuple of distinct types in order of first appearance.

    """
    if isinstance(item, Mapping):
        return _unique_types(item.values())
    if isinstance(item, Iterable) and not isinstance(
        item, (str, bytes, bytearray)
    ):
        return _unique_types(item)
    message = f"{item!r} is not a container"
    raise TypeError(message)


def collect_key_types(item: Mapping[Any, Any]) -> tuple[type, ...]:
    """Returns the distinct types of the keys in the mapping `item`.

    Args:
        item: mapping to examine.

    Raises:
        TypeError: if `item` is not a mapping.

    Returns:
        Tuple of distinct key types in order of first appearance.

    """
    if not isinstance(item, Mapping):
        message = f"{item!r} is not a mapping"
        raise TypeError(message)
    return _unique_types(item.keys())


def has_types(
    item: Any,
    kinds: type | Iterable[type],
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether the container `item` holds items of `kinds`.

    Subclasses count: an item that is a `bool` satisfies the kind `int`. For
    mappings, the values are examined.

    Args:
        item: container to examine.
        kinds: a type or an iterable of types to look for.
        raise_error: whether to raise an error if the check fails. If None,
            `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether `item` must hold every one of `kinds` (True) or any
            of them (False). If None, `miller.configuration.MATCH_ALL` is used.

    Raises:
        TypeError: if `item` is not a container.

    Returns:
        Whether `item` holds all (or any) of `kinds`.

    """
    held = collect_types(item)
    return base.has_names(
        item,
        list(utilities.iterify(kinds)),
        lambda _, k, raise_error=False: any(issubclass(h, k) for h in held),
        raise_error,
        match_all,
    )
