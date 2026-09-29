"""Introspection of the contents of folders on disk.

Names in this module are paths relative to the examined folder. For `modules`,
names are dotted paths without a suffix (for example, `package.module`).
Anything with a path component that begins with an underscore (including
`__pycache__` and `__init__.py`) is a "private" and is only included if
`include_privates` is True.

Contents:
    catalog_file_paths, collect_file_paths, has_file_paths, name_file_paths
    catalog_folder_paths, collect_folder_paths, has_folder_paths,
        name_folder_paths
    catalog_modules, collect_modules, has_modules, name_modules
    catalog_paths, collect_paths, has_paths, name_paths

"""

from __future__ import annotations

import os
import pathlib
from collections.abc import Callable
from typing import Any

from . import base, configuration, utilities

__all__: list[str] = [
    "catalog_file_paths",
    "catalog_folder_paths",
    "catalog_modules",
    "catalog_paths",
    "collect_file_paths",
    "collect_folder_paths",
    "collect_modules",
    "collect_paths",
    "has_file_paths",
    "has_folder_paths",
    "has_modules",
    "has_paths",
    "name_file_paths",
    "name_folder_paths",
    "name_modules",
    "name_paths",
]


def _relative_paths(
    item: str | os.PathLike[str],
    recursive: bool | None,
    include_privates: bool | None,
) -> tuple[pathlib.Path, list[pathlib.Path]]:
    """Returns folder `item` and sorted relative paths of its contents."""
    folder = utilities.pathlibify(item)
    if not folder.is_dir():
        message = f"{item} is not a path to a folder"
        raise NotADirectoryError(message)
    recursive = base.resolve(recursive, configuration.RECURSIVE)
    include_privates = base.resolve(
        include_privates, configuration.INCLUDE_PRIVATES
    )
    paths = folder.rglob("*") if recursive else folder.iterdir()
    relatives = sorted(p.relative_to(folder) for p in paths)
    if not include_privates:
        relatives = [
            p
            for p in relatives
            if not any(utilities.is_private_name(i) for i in p.parts)
        ]
    return folder, relatives


def _catalog(
    item: str | os.PathLike[str],
    keep: Callable[[pathlib.Path], bool],
    namer: Callable[[pathlib.Path], str],
    recursive: bool | None,
    include_privates: bool | None,
) -> dict[str, pathlib.Path]:
    """Returns dict of names and full paths of contents that pass `keep`."""
    folder, relatives = _relative_paths(item, recursive, include_privates)
    return {namer(r): folder / r for r in relatives if keep(folder / r)}


def _has(  # noqa: PLR0917
    item: str | os.PathLike[str],
    paths: Any,
    keep: Callable[[pathlib.Path], bool],
    namer: Callable[[pathlib.Path], str],
    recursive: bool | None,
    raise_error: bool | None,
    match_all: bool | None,
) -> bool:
    """Returns whether `paths` are among the contents of `item` passing `keep`.

    Each of `paths` can be a name (as returned by the `name_*` functions), a
    path relative to `item`, or a full path.
    """
    folder = utilities.pathlibify(item)
    found = _catalog(item, keep, namer, recursive, include_privates=True)

    def _checker(_: Any, path: Any, **__: Any) -> bool:
        if isinstance(path, str) and path in found:
            return True
        full = utilities.pathlibify(path)
        return any(full in (f, f.relative_to(folder)) for f in found.values())

    return base.has_names(item, paths, _checker, raise_error, match_all)


def _as_posix(path: pathlib.Path) -> str:
    """Returns the relative `path` as a str with forward slashes."""
    return path.as_posix()


def _as_module_name(path: pathlib.Path) -> str:
    """Returns the relative `path` as a dotted module name."""
    return ".".join(path.with_suffix("").parts)


def _is_module_file(path: pathlib.Path) -> bool:
    """Returns whether `path` is a python module file."""
    return path.is_file() and path.suffix in configuration.MODULE_EXTENSIONS


def name_paths(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> list[str]:
    """Returns names of everything (files and folders) in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Sorted list of paths relative to `item`, as str.

    """
    return list(catalog_paths(item, recursive, include_privates))


def collect_paths(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> list[pathlib.Path]:
    """Returns full paths of everything (files and folders) in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Sorted list of `pathlib.Path` objects.

    """
    return list(catalog_paths(item, recursive, include_privates).values())


def catalog_paths(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> dict[str, pathlib.Path]:
    """Returns dict of names and paths of everything in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Dict of relative path str names and full `pathlib.Path` objects.

    """
    return _catalog(
        item, lambda _: True, _as_posix, recursive, include_privates
    )


def has_paths(
    item: str | os.PathLike[str],
    paths: Any,
    recursive: bool | None = None,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `paths` are in folder `item`.

    Args:
        item: path to a folder.
        paths: name, path, or iterable of names or paths to look for. Each can
            be relative to `item` or a full path.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `paths` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `paths` are in `item`.

    """
    return _has(
        item,
        paths,
        lambda _: True,
        _as_posix,
        recursive,
        raise_error,
        match_all,
    )


def name_file_paths(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> list[str]:
    """Returns names of the files in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Sorted list of file paths relative to `item`, as str.

    """
    return list(catalog_file_paths(item, recursive, include_privates))


def collect_file_paths(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> list[pathlib.Path]:
    """Returns full paths of the files in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Sorted list of `pathlib.Path` objects.

    """
    return list(catalog_file_paths(item, recursive, include_privates).values())


def catalog_file_paths(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> dict[str, pathlib.Path]:
    """Returns dict of names and paths of the files in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Dict of relative path str names and full `pathlib.Path` objects.

    """
    return _catalog(
        item, lambda p: p.is_file(), _as_posix, recursive, include_privates
    )


def has_file_paths(
    item: str | os.PathLike[str],
    paths: Any,
    recursive: bool | None = None,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `paths` are files in folder `item`.

    Args:
        item: path to a folder.
        paths: name, path, or iterable of names or paths to look for. Each can
            be relative to `item` or a full path.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `paths` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `paths` are files in `item`.

    """
    return _has(
        item,
        paths,
        lambda p: p.is_file(),
        _as_posix,
        recursive,
        raise_error,
        match_all,
    )


def name_folder_paths(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> list[str]:
    """Returns names of the folders in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Sorted list of folder paths relative to `item`, as str.

    """
    return list(catalog_folder_paths(item, recursive, include_privates))


def collect_folder_paths(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> list[pathlib.Path]:
    """Returns full paths of the folders in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Sorted list of `pathlib.Path` objects.

    """
    return list(
        catalog_folder_paths(item, recursive, include_privates).values()
    )


def catalog_folder_paths(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> dict[str, pathlib.Path]:
    """Returns dict of names and paths of the folders in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Dict of relative path str names and full `pathlib.Path` objects.

    """
    return _catalog(
        item, lambda p: p.is_dir(), _as_posix, recursive, include_privates
    )


def has_folder_paths(
    item: str | os.PathLike[str],
    paths: Any,
    recursive: bool | None = None,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `paths` are folders in folder `item`.

    Args:
        item: path to a folder.
        paths: name, path, or iterable of names or paths to look for. Each can
            be relative to `item` or a full path.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `paths` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `paths` are folders in `item`.

    """
    return _has(
        item,
        paths,
        lambda p: p.is_dir(),
        _as_posix,
        recursive,
        raise_error,
        match_all,
    )


def name_modules(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> list[str]:
    """Returns names of the python modules in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Sorted list of dotted module names relative to `item`.

    """
    return list(catalog_modules(item, recursive, include_privates))


def collect_modules(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> list[pathlib.Path]:
    """Returns full paths of the python modules in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Sorted list of `pathlib.Path` objects.

    """
    return list(catalog_modules(item, recursive, include_privates).values())


def catalog_modules(
    item: str | os.PathLike[str],
    recursive: bool | None = None,
    include_privates: bool | None = None,
) -> dict[str, pathlib.Path]:
    """Returns dict of names and paths of the python modules in folder `item`.

    Args:
        item: path to a folder.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        include_privates: whether to include paths with a component beginning
            with an underscore. If None, `miller.configuration.INCLUDE_PRIVATES`
            is used.

    Raises:
        NotADirectoryError: if `item` is not a folder.

    Returns:
        Dict of dotted module names and full `pathlib.Path` objects.

    """
    return _catalog(
        item, _is_module_file, _as_module_name, recursive, include_privates
    )


def has_modules(
    item: str | os.PathLike[str],
    paths: Any,
    recursive: bool | None = None,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `paths` are python modules in folder `item`.

    Args:
        item: path to a folder.
        paths: module name, path, or iterable of names or paths to look for.
            Each can be a dotted module name, relative to `item`, or a full
            path.
        recursive: whether to include subfolders. If None,
            `miller.configuration.RECURSIVE` is used.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `paths` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `paths` are python modules in `item`.

    """
    return _has(
        item,
        paths,
        _is_module_file,
        _as_module_name,
        recursive,
        raise_error,
        match_all,
    )
