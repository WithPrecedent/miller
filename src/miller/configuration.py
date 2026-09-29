"""Global default settings for miller.

Every setting here is only a default. Any function that accepts an argument
covering the same setting (for example, `include_privates`) will always use the
argument, when passed, in preference to the global setting. Use the `set_*`
functions in `miller.framework` to change these settings safely.

Attributes:
    INCLUDE_PRIVATES: whether names beginning with an underscore are included
        in results.
    INCLUDE_STR: whether `str` objects count as containers, iterables, and
        sequences.
    KEYER: function used to determine a str name for an item.
    MATCH_ALL: whether all (True) or any (False) of the sought items must be
        found by `has_*` functions.
    MODULE_EXTENSIONS: file suffixes that identify python modules.
    RAISE_ERRORS: whether `has_*` and `is_*` functions raise an error (True) or
        just return False (False) when an item does not qualify.
    RECURSIVE: whether functions that examine folders also examine subfolders.

"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from . import utilities

INCLUDE_PRIVATES: bool = False
INCLUDE_STR: bool = False
KEYER: Callable[[Any], str] = utilities.namify
MATCH_ALL: bool = True
MODULE_EXTENSIONS: tuple[str, ...] = (".py",)
RAISE_ERRORS: bool = False
RECURSIVE: bool = False
