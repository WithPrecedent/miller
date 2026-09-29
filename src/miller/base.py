"""Shared machinery for miller's introspection functions.

Contents:
    resolve: returns an argument or, if it is None, a global setting.
    verdict: returns a check result or raises an error when it failed.
    has_names: implements the `has_*` functions.
    membership: returns a `has_names` checker based on a container of names.
    name_where: implements the `name_*` functions for attribute-like kinds.
    catalog_where: implements the `catalog_*` functions.

"""

from __future__ import annotations

from collections.abc import Callable, Container, Iterable
from typing import Any, TypeVar

from . import configuration, utilities

_T = TypeVar('_T')


def resolve(value: _T | None, default: _T) -> _T:
    """Returns `value` unless it is None, in which case `default` is returned.

    Args:
        value: argument passed by a user.
        default: global setting to use when `value` is None.

    Returns:
        `value` or `default`.

    """
    return default if value is None else value


def verdict(
    value: bool,
    raise_error: bool | None,
    message: str,
    error: type[Exception] = TypeError) -> bool:
    """Returns `value` or raises an error if `value` is False.

    Args:
        value: result of a check.
        raise_error: whether to raise an error if `value` is False. If None,
            `miller.configuration.RAISE_ERRORS` is used.
        message: message for the error, if one is raised.
        error: type of error to raise. Defaults to `TypeError`.

    Raises:
        Exception: `error` if `value` is False and errors should be raised.

    Returns:
        `value`.

    """
    if not value and resolve(raise_error, configuration.RAISE_ERRORS):
        raise error(message)
    return bool(value)


def has_names(
    item: Any,
    names: Any,
    checker: Callable[..., bool],
    raise_error: bool | None = None,
    match_all: bool | None = None) -> bool:
    """Returns whether `names` qualify in `item` according to `checker`.

    Args:
        item: object to examine.
        names: str name or iterable of str names to check.
        checker: function that takes `item` and one name and returns whether
            that name qualifies as the sought kind of element of `item`. It is
            always called with `raise_error = False`, so that only the final
            result of all the checks can raise an error.
        raise_error: whether to raise an error if the check fails. If None,
            `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must qualify (True) or any of them
            (False). If None, `miller.configuration.MATCH_ALL` is used.

    Raises:
        AttributeError: if the check fails and errors should be raised.

    Returns:
        Whether all or any (depending on `match_all`) `names` qualify.

    """
    names = list(utilities.iterify(names))
    match_all = resolve(match_all, configuration.MATCH_ALL)
    scope = all if match_all else any
    value = scope(checker(item, n, raise_error = False) for n in names)
    quantifier = 'Not all' if match_all else 'None'
    return verdict(
        value = value,
        raise_error = raise_error,
        message = f'{quantifier} of {names} qualify in {item!r}',
        error = AttributeError)


def membership(collection: Container[Any]) -> Callable[..., bool]:
    """Returns a checker for `has_names` that tests membership in `collection`.

    Args:
        collection: container of names that qualify.

    Returns:
        Function that takes an item, a name, and `raise_error` and returns
            whether the name is in `collection`.

    """
    return lambda _, name, raise_error = False: name in collection


def name_where(
    names: Iterable[str],
    predicate: Callable[[str], bool],
    include_privates: bool | None = None) -> list[str]:
    """Returns the `names` that satisfy `predicate`.

    Args:
        names: str names to filter.
        predicate: function that takes a name and returns whether to keep it.
        include_privates: whether to keep names beginning with an underscore.
            If None, `miller.configuration.INCLUDE_PRIVATES` is used.

    Returns:
        List of the selected names in their original order.

    """
    include_privates = resolve(
        include_privates, configuration.INCLUDE_PRIVATES)
    return [
        n for n in names
        if (include_privates or not utilities.is_private_name(n))
        and predicate(n)]


def catalog_where(
    names: Iterable[str],
    predicate: Callable[[str], bool],
    getter: Callable[[str], Any],
    include_privates: bool | None = None) -> dict[str, Any]:
    """Returns a dict of the `names` satisfying `predicate` and their values.

    Args:
        names: str names to filter.
        predicate: function that takes a name and returns whether to keep it.
        getter: function that takes a name and returns its value.
        include_privates: whether to keep names beginning with an underscore.
            If None, `miller.configuration.INCLUDE_PRIVATES` is used.

    Returns:
        Dict with the selected names as keys and their values as values.

    """
    selected = name_where(
        names = names,
        predicate = predicate,
        include_privates = include_privates)
    return {n: getter(n) for n in selected}
