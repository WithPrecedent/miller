"""Functions for changing miller's global default settings.

The settings themselves are stored in `miller.configuration`. An argument
passed directly to any function always takes precedence over these defaults.

Contents:
    set_include_privates: sets whether names beginning with '_' are included.
    set_include_str: sets whether `str` counts as a container or iterable.
    set_keyer: sets the function used to name items.
    set_match_all: sets whether `has_*` functions require all names to match.
    set_module_extensions: sets the file suffixes of python modules.
    set_raise_errors: sets whether `has_*` and `is_*` functions raise errors.
    set_recursion: sets whether folder functions include subfolders.

"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from . import configuration

__all__: list[str] = [
    'set_include_privates',
    'set_include_str',
    'set_keyer',
    'set_match_all',
    'set_module_extensions',
    'set_raise_errors',
    'set_recursion']


def _set_bool(name: str, value: Any) -> None:
    """Sets the boolean setting `name` in `miller.configuration`."""
    if not isinstance(value, bool):
        message = f'{name.lower()} argument must be a boolean type'
        raise TypeError(message)
    setattr(configuration, name, value)


def set_include_privates(include_privates: bool) -> None:
    """Sets the global default for including names beginning with '_'.

    Args:
        include_privates: value to set `INCLUDE_PRIVATES` to.

    Raises:
        TypeError: if `include_privates` is not a boolean type.

    """
    _set_bool('INCLUDE_PRIVATES', include_privates)


def set_include_str(include_str: bool) -> None:
    """Sets the global default for whether `str` counts as a container.

    Args:
        include_str: value to set `INCLUDE_STR` to.

    Raises:
        TypeError: if `include_str` is not a boolean type.

    """
    _set_bool('INCLUDE_STR', include_str)


def set_keyer(keyer: Callable[[Any], str]) -> None:
    """Sets the global default function used to name items.

    Args:
        keyer: function that returns a str name of any item passed.

    Raises:
        TypeError: if `keyer` is not callable.

    """
    if not callable(keyer):
        message = 'keyer argument must be callable'
        raise TypeError(message)
    configuration.KEYER = keyer


def set_match_all(match_all: bool) -> None:
    """Sets the global default for whether all names must match in `has_*`.

    Args:
        match_all: value to set `MATCH_ALL` to.

    Raises:
        TypeError: if `match_all` is not a boolean type.

    """
    _set_bool('MATCH_ALL', match_all)


def set_module_extensions(extensions: Sequence[str]) -> None:
    """Sets the global default file suffixes of python modules.

    Args:
        extensions: file suffixes of python modules (for example, '.py').

    Raises:
        TypeError: if `extensions` is not a sequence of str type.

    """
    if (
            isinstance(extensions, Sequence)
            and not isinstance(extensions, str)
            and all(isinstance(i, str) for i in extensions)):
        configuration.MODULE_EXTENSIONS = tuple(extensions)
    else:
        message = 'extensions argument must be a sequence of strings'
        raise TypeError(message)


def set_raise_errors(raise_errors: bool) -> None:
    """Sets the global default for raising errors from `has_*` and `is_*`.

    Args:
        raise_errors: value to set `RAISE_ERRORS` to.

    Raises:
        TypeError: if `raise_errors` is not a boolean type.

    """
    _set_bool('RAISE_ERRORS', raise_errors)


def set_recursion(recursive: bool) -> None:
    """Sets the global default rule whether tools should be recursive.

    If a `recursive` argument is passed to a function that takes one, that
    argument will always take precedence. However, the default value is used
    when an argument is not passed.

    Args:
        recursive: value to set `RECURSIVE` to.

    Raises:
        TypeError: if `recursive` is not a boolean type.

    """
    _set_bool('RECURSIVE', recursive)
