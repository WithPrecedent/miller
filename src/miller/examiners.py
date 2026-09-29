"""Object-oriented introspection using inspector classes.

`Inspector` is a factory: calling it with a module, path, class, or object
returns the appropriate subclass (`ModuleInspector`, `PackageInspector`,
`ClassInspector`, or `InstanceInspector`). Each inspector exposes the results
of the corresponding `name_*`, `collect_*`, and `catalog_*` functions as
properties.

Contents:
    Inspector: factory and base class.
    ClassInspector: inspector for classes.
    InstanceInspector: inspector for class instances.
    ModuleInspector: inspector for python modules.
    PackageInspector: inspector for folders of python modules.

"""

from __future__ import annotations

import inspect
import os
import pathlib
import types
from typing import Any

from . import attributes, containers, disks, modules, utilities

__all__: list[str] = [
    "ClassInspector",
    "Inspector",
    "InstanceInspector",
    "ModuleInspector",
    "PackageInspector",
]


class Inspector:
    """Inspector factory which returns the appropriate Inspector subclass.

    Args:
        item: unknown item to examine.
        include_privates: whether to include names that begin with an
            underscore. Defaults to False.

    """

    def __new__(  # noqa: PYI034
        cls, item: Any, *args: Any, **kwargs: Any
    ) -> Inspector:
        """Returns an Inspector subclass instance based on type of `item`."""
        if cls is not Inspector:
            return super().__new__(cls)
        if isinstance(item, types.ModuleType):
            subclass: type[Inspector] = ModuleInspector
        elif isinstance(item, (pathlib.Path, str, os.PathLike)):
            subclass = PackageInspector
        elif inspect.isclass(item):
            subclass = ClassInspector
        else:
            subclass = InstanceInspector
        return super().__new__(subclass)

    def __init__(self, item: Any, *, include_privates: bool = False) -> None:
        self.item = item
        self.include_privates = include_privates

    def __repr__(self) -> str:
        """Returns a representation of the inspector."""
        return f"{self.__class__.__name__}(item={self.item!r})"

    @property
    def name(self) -> str:
        """Str name of the examined item."""
        return utilities.namify(self.item)

    @property
    def type(self) -> type:
        """Data type of the examined item."""
        return type(self.item)


class _AttributeInspector(Inspector):
    """Base class for inspectors of things with attributes."""

    @property
    def annotations(self) -> dict[str, Any]:
        """Names and type annotations."""
        return attributes.catalog_annotations(self.item, self.include_privates)

    @property
    def attributes(self) -> dict[str, Any]:
        """Names and values of all attributes."""
        return attributes.catalog_attributes(self.item, self.include_privates)

    @property
    def methods(self) -> dict[str, Any]:
        """Names and values of methods."""
        return attributes.catalog_methods(self.item, self.include_privates)

    @property
    def signatures(self) -> dict[str, inspect.Signature]:
        """Names and signatures of methods."""
        return attributes.catalog_signatures(self.item, self.include_privates)

    @property
    def variables(self) -> dict[str, Any]:
        """Names and values of attributes that are not methods or properties."""
        return attributes.catalog_variables(self.item, self.include_privates)


class _ObjectInspector(_AttributeInspector):
    """Base class for inspectors of classes and instances."""

    @property
    def contains(self) -> tuple[type, ...] | None:
        """Types of items held by the examined item, if it is a container."""
        try:
            return containers.collect_types(self.item)
        except TypeError:
            return None

    @property
    def fields(self) -> dict[str, Any]:
        """Names and `dataclasses.Field` objects if `item` is a dataclass."""
        try:
            return attributes.catalog_fields(self.item, self.include_privates)
        except TypeError:
            return {}

    @property
    def properties(self) -> dict[str, Any]:
        """Names and values of properties."""
        return attributes.catalog_properties(self.item, self.include_privates)


class ClassInspector(_ObjectInspector):
    """Inspector for classes.

    Args:
        item: class to examine.
        include_privates: whether to include names that begin with an
            underscore. Defaults to False.

    """

    @property
    def class_attributes(self) -> dict[str, Any]:
        """Names and values of class attributes."""
        return attributes.catalog_class_attributes(
            self.item, self.include_privates
        )

    @property
    def parameters(self) -> list[str]:
        """Names of annotated parameters (as in a dataclass)."""
        return attributes.name_annotations(self.item, self.include_privates)


class InstanceInspector(_ObjectInspector):
    """Inspector for class instances.

    Args:
        item: object to examine.
        include_privates: whether to include names that begin with an
            underscore. Defaults to False.

    """

    @property
    def class_attributes(self) -> dict[str, Any]:
        """Names and values of attributes of the class of the instance."""
        return attributes.catalog_class_attributes(
            self.item, self.include_privates
        )

    @property
    def instance_attributes(self) -> dict[str, Any]:
        """Names and values of attributes stored on the instance."""
        return attributes.catalog_instance_attributes(
            self.item, self.include_privates
        )


class ModuleInspector(_AttributeInspector):
    """Inspector for python modules.

    Args:
        item: module to examine.
        include_privates: whether to include names that begin with an
            underscore. Defaults to False.

    """

    @property
    def classes(self) -> dict[str, type]:
        """Names and classes defined in the module."""
        return modules.catalog_classes(self.item, self.include_privates)

    @property
    def functions(self) -> dict[str, types.FunctionType]:
        """Names and functions defined in the module."""
        return modules.catalog_functions(self.item, self.include_privates)


class PackageInspector(Inspector):
    """Inspector for folders (for example, python packages).

    Args:
        item: path to a folder.
        include_privates: whether to include paths with a component beginning
            with an underscore. Defaults to False.
        recursive: whether to include subfolders. Defaults to True.

    """

    def __init__(
        self,
        item: str | os.PathLike[str],
        *,
        include_privates: bool = False,
        recursive: bool = True,
    ) -> None:
        super().__init__(
            utilities.pathlibify(item), include_privates=include_privates
        )
        self.recursive = recursive

    @property
    def file_paths(self) -> dict[str, pathlib.Path]:
        """Names and paths of files in the folder."""
        return disks.catalog_file_paths(
            self.item, self.recursive, self.include_privates
        )

    @property
    def folder_paths(self) -> dict[str, pathlib.Path]:
        """Names and paths of folders in the folder."""
        return disks.catalog_folder_paths(
            self.item, self.recursive, self.include_privates
        )

    @property
    def modules(self) -> dict[str, pathlib.Path]:
        """Names and paths of python modules in the folder."""
        return disks.catalog_modules(
            self.item, self.recursive, self.include_privates
        )

    @property
    def paths(self) -> dict[str, pathlib.Path]:
        """Names and paths of everything in the folder."""
        return disks.catalog_paths(
            self.item, self.recursive, self.include_privates
        )
