"""Introspection of the attributes of classes, instances, and modules.

Each kind of attribute has functions with the following prefixes:

    catalog: returns a dict of names and values.
    collect: returns a list of values.
    has: returns whether specified names are of that kind.
    name: returns a list of str names.

The kinds are: `annotations`, `attributes`, `class_attributes`, `fields`,
`instance_attributes`, `methods`, `properties`, `signatures`, and `variables`.
Singular `is_*` functions (for example, `is_method`) check a single name.

Contents:
    is_attribute, is_class_attribute, is_field, is_instance_attribute,
    is_method, is_property, is_variable
    catalog_*, collect_*, has_*, name_* for each of the kinds above.

"""

from __future__ import annotations

import dataclasses
import functools
import inspect
import types
from collections.abc import Callable
from typing import Any

from . import base

__all__: list[str] = [
    "catalog_annotations",
    "catalog_attributes",
    "catalog_class_attributes",
    "catalog_fields",
    "catalog_instance_attributes",
    "catalog_methods",
    "catalog_properties",
    "catalog_signatures",
    "catalog_variables",
    "collect_annotations",
    "collect_attributes",
    "collect_class_attributes",
    "collect_fields",
    "collect_instance_attributes",
    "collect_methods",
    "collect_properties",
    "collect_signatures",
    "collect_variables",
    "has_annotations",
    "has_attributes",
    "has_class_attributes",
    "has_fields",
    "has_instance_attributes",
    "has_methods",
    "has_properties",
    "has_signatures",
    "has_variables",
    "is_attribute",
    "is_class_attribute",
    "is_field",
    "is_instance_attribute",
    "is_method",
    "is_property",
    "is_variable",
    "name_annotations",
    "name_attributes",
    "name_class_attributes",
    "name_fields",
    "name_instance_attributes",
    "name_methods",
    "name_properties",
    "name_signatures",
    "name_variables",
]

_MISSING: Any = object()
_PROPERTY_TYPES: tuple[type, ...] = (property, functools.cached_property)


def _static(item: Any, name: str) -> Any:
    """Returns attribute `name` of `item` without running any descriptors."""
    try:
        return inspect.getattr_static(item, name)
    except AttributeError:
        return _MISSING


def _value(item: Any, name: str) -> Any:
    """Returns the value of `name` in `item`.

    If getting the value fails (as can happen with a property that raises an
    error), the raw attribute is returned instead.
    """
    try:
        return getattr(item, name)
    except Exception:  # noqa: BLE001
        return _static(item, name)


def _is_routine(raw: Any) -> bool:
    """Returns whether `raw` (a statically found attribute) is a method."""
    return isinstance(raw, (classmethod, staticmethod)) or inspect.isroutine(
        raw
    )


def is_attribute(item: Any, name: str, raise_error: bool | None = None) -> bool:
    """Returns whether `name` is an attribute of `item`.

    Args:
        item: class, instance, or module to examine.
        name: str name of the attribute.
        raise_error: whether to raise an `AttributeError` if `name` is not an
            attribute. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `name` is an attribute of `item`.

    """
    value = _static(item, name) is not _MISSING
    if not value:
        try:
            value = hasattr(item, name)
        except Exception:  # noqa: BLE001
            value = False
    return base.verdict(
        value,
        raise_error,
        f"{name} is not an attribute of {item!r}",
        AttributeError,
    )


def is_class_attribute(
    item: Any, name: str, raise_error: bool | None = None
) -> bool:
    """Returns whether `name` is an attribute of the class of `item`.

    Args:
        item: class or instance to examine.
        name: str name of the attribute.
        raise_error: whether to raise an `AttributeError` if `name` is not a
            class attribute. If None, `miller.configuration.RAISE_ERRORS` is
            used.

    Returns:
        Whether `name` is defined on the class (or a parent class).

    """
    cls = item if inspect.isclass(item) else item.__class__
    return base.verdict(
        _static(cls, name) is not _MISSING,
        raise_error,
        f"{name} is not a class attribute of {item!r}",
        AttributeError,
    )


def is_field(item: Any, name: str, raise_error: bool | None = None) -> bool:
    """Returns whether `name` is a field of the dataclass `item`.

    Args:
        item: dataclass or dataclass instance to examine.
        name: str name of the field.
        raise_error: whether to raise an `AttributeError` if `name` is not a
            field. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `name` is a field of `item`. This is False if `item` is not a
            dataclass.

    """
    value = dataclasses.is_dataclass(item) and name in {
        f.name for f in dataclasses.fields(item)
    }
    return base.verdict(
        value, raise_error, f"{name} is not a field of {item!r}", AttributeError
    )


def is_instance_attribute(
    item: Any, name: str, raise_error: bool | None = None
) -> bool:
    """Returns whether `name` is an attribute stored on the instance `item`.

    Args:
        item: instance to examine. A class always returns False.
        name: str name of the attribute.
        raise_error: whether to raise an `AttributeError` if `name` is not an
            instance attribute. If None, `miller.configuration.RAISE_ERRORS` is
            used.

    Returns:
        Whether `name` is in the `__dict__` of `item` or is a filled slot.

    """
    value = False
    if not inspect.isclass(item):
        if name in getattr(item, "__dict__", {}):
            value = True
        else:
            raw = _static(item.__class__, name)
            value = (
                isinstance(raw, types.MemberDescriptorType)
                and _static(item, name) is not _MISSING
                and hasattr(item, name)
            )
    return base.verdict(
        value,
        raise_error,
        f"{name} is not an instance attribute of {item!r}",
        AttributeError,
    )


def is_method(item: Any, name: str, raise_error: bool | None = None) -> bool:
    """Returns whether `name` is a method (or function) of `item`.

    Args:
        item: class, instance, or module to examine.
        name: str name of the attribute.
        raise_error: whether to raise an `AttributeError` if `name` is not a
            method. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `name` is an attribute of `item` that is a function, method,
            classmethod, or staticmethod. A callable stored in the `__dict__`
            of an instance is not a method.

    """
    raw = _static(item, name)
    value = _is_routine(raw)
    if value and not inspect.isclass(item) and not inspect.ismodule(item):
        value = name not in getattr(item, "__dict__", {})
    return base.verdict(
        value,
        raise_error,
        f"{name} is not a method of {item!r}",
        AttributeError,
    )


def is_property(item: Any, name: str, raise_error: bool | None = None) -> bool:
    """Returns whether `name` is a property of `item`.

    Args:
        item: class or instance to examine.
        name: str name of the attribute.
        raise_error: whether to raise an `AttributeError` if `name` is not a
            property. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `name` is a `property` (or `functools.cached_property`).

    """
    return base.verdict(
        isinstance(_static(item, name), _PROPERTY_TYPES),
        raise_error,
        f"{name} is not a property of {item!r}",
        AttributeError,
    )


def is_variable(item: Any, name: str, raise_error: bool | None = None) -> bool:
    """Returns whether `name` is an attribute that is not a method or property.

    Args:
        item: class, instance, or module to examine.
        name: str name of the attribute.
        raise_error: whether to raise an `AttributeError` if `name` is not a
            variable. If None, `miller.configuration.RAISE_ERRORS` is used.

    Returns:
        Whether `name` is an attribute of `item` that is neither a method nor a
            property.

    """
    value = (
        is_attribute(item, name, raise_error=False)
        and not is_method(item, name, raise_error=False)
        and not is_property(item, name, raise_error=False)
    )
    return base.verdict(
        value,
        raise_error,
        f"{name} is not a variable of {item!r}",
        AttributeError,
    )


""" Names (the str names of attributes of each kind) """


def _names(
    item: Any,
    checker: Callable[[Any, str], bool],
    include_privates: bool | None,
) -> list[str]:
    """Returns names in `dir(item)` that `checker` accepts."""
    return base.name_where(
        names=dir(item),
        predicate=functools.partial(checker, item),
        include_privates=include_privates,
    )


def _catalog(
    item: Any,
    checker: Callable[[Any, str], bool],
    include_privates: bool | None,
) -> dict[str, Any]:
    """Returns dict of names in `dir(item)` accepted by `checker`."""
    return base.catalog_where(
        names=dir(item),
        predicate=functools.partial(checker, item),
        getter=functools.partial(_value, item),
        include_privates=include_privates,
    )


def name_attributes(
    item: Any, include_privates: bool | None = None
) -> list[str]:
    """Returns names of the attributes of `item`.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of attribute names.

    """
    return _names(item, is_attribute, include_privates)


def collect_attributes(
    item: Any, include_privates: bool | None = None
) -> list[Any]:
    """Returns the values of the attributes of `item`.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include attributes whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of attribute values.

    """
    return list(catalog_attributes(item, include_privates).values())


def catalog_attributes(
    item: Any, include_privates: bool | None = None
) -> dict[str, Any]:
    """Returns a dict of the names and values of the attributes of `item`.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include attributes whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        Dict of attribute names and values.

    """
    return _catalog(item, is_attribute, include_privates)


def has_attributes(
    item: Any,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `names` are attributes of `item`.

    Args:
        item: class, instance, or module to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `names` are attributes of `item`.

    """
    return base.has_names(item, names, is_attribute, raise_error, match_all)


def name_class_attributes(
    item: Any, include_privates: bool | None = None
) -> list[str]:
    """Returns names of the attributes defined on the class of `item`.

    Args:
        item: class or instance to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of class attribute names.

    """
    cls = item if inspect.isclass(item) else item.__class__
    return _names(cls, is_class_attribute, include_privates)


def collect_class_attributes(
    item: Any, include_privates: bool | None = None
) -> list[Any]:
    """Returns the values of the attributes defined on the class of `item`.

    Args:
        item: class or instance to examine.
        include_privates: whether to include attributes whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of class attribute values.

    """
    return list(catalog_class_attributes(item, include_privates).values())


def catalog_class_attributes(
    item: Any, include_privates: bool | None = None
) -> dict[str, Any]:
    """Returns dict of names and values of the class attributes of `item`.

    Args:
        item: class or instance to examine.
        include_privates: whether to include attributes whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        Dict of class attribute names and values.

    """
    cls = item if inspect.isclass(item) else item.__class__
    return _catalog(cls, is_class_attribute, include_privates)


def has_class_attributes(
    item: Any,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `names` are class attributes of `item`.

    Args:
        item: class or instance to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `names` are class attributes of `item`.

    """
    return base.has_names(
        item, names, is_class_attribute, raise_error, match_all
    )


def name_fields(item: Any, include_privates: bool | None = None) -> list[str]:
    """Returns names of the fields of the dataclass `item`.

    Args:
        item: dataclass or dataclass instance to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Raises:
        TypeError: if `item` is not a dataclass.

    Returns:
        List of field names.

    """
    return list(catalog_fields(item, include_privates))


def collect_fields(
    item: Any, include_privates: bool | None = None
) -> list[dataclasses.Field[Any]]:
    """Returns the `dataclasses.Field` objects of the dataclass `item`.

    Args:
        item: dataclass or dataclass instance to examine.
        include_privates: whether to include fields whose names begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Raises:
        TypeError: if `item` is not a dataclass.

    Returns:
        List of fields.

    """
    return list(catalog_fields(item, include_privates).values())


def catalog_fields(
    item: Any, include_privates: bool | None = None
) -> dict[str, dataclasses.Field[Any]]:
    """Returns dict of names and `dataclasses.Field` objects of `item`.

    Args:
        item: dataclass or dataclass instance to examine.
        include_privates: whether to include fields whose names begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Raises:
        TypeError: if `item` is not a dataclass.

    Returns:
        Dict of field names and fields.

    """
    if not dataclasses.is_dataclass(item):
        message = f"{item!r} is not a dataclass"
        raise TypeError(message)
    fields = {f.name: f for f in dataclasses.fields(item)}
    return base.catalog_where(
        names=fields,
        predicate=lambda _: True,
        getter=fields.__getitem__,
        include_privates=include_privates,
    )


def has_fields(
    item: Any,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `names` are fields of the dataclass `item`.

    Args:
        item: dataclass or dataclass instance to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Raises:
        TypeError: if `item` is not a dataclass.

    Returns:
        Whether all (or any) of `names` are fields of `item`.

    """
    if not dataclasses.is_dataclass(item):
        message = f"{item!r} is not a dataclass"
        raise TypeError(message)
    return base.has_names(item, names, is_field, raise_error, match_all)


def name_instance_attributes(
    item: Any, include_privates: bool | None = None
) -> list[str]:
    """Returns names of the attributes stored on the instance `item`.

    Args:
        item: instance to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of instance attribute names.

    """
    return _names(item, is_instance_attribute, include_privates)


def collect_instance_attributes(
    item: Any, include_privates: bool | None = None
) -> list[Any]:
    """Returns the values of the attributes stored on the instance `item`.

    Args:
        item: instance to examine.
        include_privates: whether to include attributes whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of instance attribute values.

    """
    return list(catalog_instance_attributes(item, include_privates).values())


def catalog_instance_attributes(
    item: Any, include_privates: bool | None = None
) -> dict[str, Any]:
    """Returns dict of names and values of the instance attributes of `item`.

    Args:
        item: instance to examine.
        include_privates: whether to include attributes whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        Dict of instance attribute names and values.

    """
    return _catalog(item, is_instance_attribute, include_privates)


def has_instance_attributes(
    item: Any,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `names` are instance attributes of `item`.

    Args:
        item: instance to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `names` are instance attributes of `item`.

    """
    return base.has_names(
        item, names, is_instance_attribute, raise_error, match_all
    )


def name_methods(item: Any, include_privates: bool | None = None) -> list[str]:
    """Returns names of the methods of `item`.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of method names.

    """
    return _names(item, is_method, include_privates)


def collect_methods(
    item: Any, include_privates: bool | None = None
) -> list[Any]:
    """Returns the methods of `item`.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include methods whose names begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of methods.

    """
    return list(catalog_methods(item, include_privates).values())


def catalog_methods(
    item: Any, include_privates: bool | None = None
) -> dict[str, Any]:
    """Returns a dict of the names and methods of `item`.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include methods whose names begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        Dict of method names and methods.

    """
    return _catalog(item, is_method, include_privates)


def has_methods(
    item: Any,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `names` are methods of `item`.

    Args:
        item: class, instance, or module to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `names` are methods of `item`.

    """
    return base.has_names(item, names, is_method, raise_error, match_all)


def name_properties(
    item: Any, include_privates: bool | None = None
) -> list[str]:
    """Returns names of the properties of `item`.

    Args:
        item: class or instance to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of property names.

    """
    return _names(item, is_property, include_privates)


def collect_properties(
    item: Any, include_privates: bool | None = None
) -> list[Any]:
    """Returns the values of the properties of `item`.

    Args:
        item: class or instance to examine. If `item` is a class, the
            `property` objects themselves are returned.
        include_privates: whether to include properties whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of property values.

    """
    return list(catalog_properties(item, include_privates).values())


def catalog_properties(
    item: Any, include_privates: bool | None = None
) -> dict[str, Any]:
    """Returns a dict of the names and values of the properties of `item`.

    Args:
        item: class or instance to examine. If `item` is a class, the
            `property` objects themselves are the values.
        include_privates: whether to include properties whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        Dict of property names and values.

    """
    return _catalog(item, is_property, include_privates)


def has_properties(
    item: Any,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `names` are properties of `item`.

    Args:
        item: class or instance to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `names` are properties of `item`.

    """
    return base.has_names(item, names, is_property, raise_error, match_all)


def name_variables(
    item: Any, include_privates: bool | None = None
) -> list[str]:
    """Returns names of the variables of `item`.

    Variables are attributes that are neither methods nor properties.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of variable names.

    """
    return _names(item, is_variable, include_privates)


def collect_variables(
    item: Any, include_privates: bool | None = None
) -> list[Any]:
    """Returns the values of the variables of `item`.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include variables whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of variable values.

    """
    return list(catalog_variables(item, include_privates).values())


def catalog_variables(
    item: Any, include_privates: bool | None = None
) -> dict[str, Any]:
    """Returns a dict of the names and values of the variables of `item`.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include variables whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        Dict of variable names and values.

    """
    return _catalog(item, is_variable, include_privates)


def has_variables(
    item: Any,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `names` are variables of `item`.

    Args:
        item: class, instance, or module to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `names` are variables of `item`.

    """
    return base.has_names(item, names, is_variable, raise_error, match_all)


""" Signatures """


def _signatures(item: Any) -> dict[str, inspect.Signature]:
    """Returns all signatures for callables in `item` that have signatures."""
    signatures = {}
    for name in dir(item):
        if not is_method(item, name):
            continue
        try:
            signatures[name] = inspect.signature(getattr(item, name))
        except (TypeError, ValueError):
            continue
    return signatures


def name_signatures(
    item: Any, include_privates: bool | None = None
) -> list[str]:
    """Returns names of the methods of `item` that have signatures.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of names of methods with retrievable signatures.

    """
    return list(catalog_signatures(item, include_privates))


def collect_signatures(
    item: Any, include_privates: bool | None = None
) -> list[inspect.Signature]:
    """Returns the signatures of the methods of `item`.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include methods whose names begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of `inspect.Signature` objects.

    """
    return list(catalog_signatures(item, include_privates).values())


def catalog_signatures(
    item: Any, include_privates: bool | None = None
) -> dict[str, inspect.Signature]:
    """Returns a dict of the names and signatures of the methods of `item`.

    Args:
        item: class, instance, or module to examine.
        include_privates: whether to include methods whose names begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        Dict of method names and `inspect.Signature` objects.

    """
    signatures = _signatures(item)
    return base.catalog_where(
        names=signatures,
        predicate=lambda _: True,
        getter=signatures.__getitem__,
        include_privates=include_privates,
    )


def has_signatures(
    item: Any,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `names` are methods of `item` with signatures.

    Args:
        item: class, instance, or module to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `names` have signatures in `item`.

    """
    return base.has_names(
        item, names, base.membership(_signatures(item)), raise_error, match_all
    )


""" Annotations """


def _annotations(item: Any) -> dict[str, Any]:
    """Returns type annotations of `item` without evaluating strings.

    Annotations are gathered across the whole inheritance chain of a class
    (children override parents) and, for instances, from the instance as well.
    """
    if inspect.isclass(item):
        annotations: dict[str, Any] = {}
        for cls in reversed(item.__mro__):
            annotations.update(inspect.get_annotations(cls))
        return annotations
    if inspect.ismodule(item) or inspect.isroutine(item):
        return dict(inspect.get_annotations(item))
    annotations = _annotations(item.__class__)
    annotations.update(getattr(item, "__annotations__", {}) or {})
    return annotations


def name_annotations(
    item: Any, include_privates: bool | None = None
) -> list[str]:
    """Returns names of the annotated attributes or parameters of `item`.

    Args:
        item: class, instance, module, or function to examine.
        include_privates: whether to include names that begin with an
            underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of names that have type annotations.

    """
    return list(catalog_annotations(item, include_privates))


def collect_annotations(
    item: Any, include_privates: bool | None = None
) -> list[Any]:
    """Returns the type annotations of `item`.

    Args:
        item: class, instance, module, or function to examine.
        include_privates: whether to include annotations whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        List of annotations (which are `str` if the annotated code uses
            `from __future__ import annotations`).

    """
    return list(catalog_annotations(item, include_privates).values())


def catalog_annotations(
    item: Any, include_privates: bool | None = None
) -> dict[str, Any]:
    """Returns a dict of the names and type annotations of `item`.

    Args:
        item: class, instance, module, or function to examine.
        include_privates: whether to include annotations whose names begin with
            an underscore. If None, `miller.configuration.INCLUDE_PRIVATES` is
            used.

    Returns:
        Dict of annotated names and their annotations.

    """
    annotations = _annotations(item)
    return base.catalog_where(
        names=annotations,
        predicate=lambda _: True,
        getter=annotations.__getitem__,
        include_privates=include_privates,
    )


def has_annotations(
    item: Any,
    names: Any,
    raise_error: bool | None = None,
    match_all: bool | None = None,
) -> bool:
    """Returns whether `names` have type annotations in `item`.

    Args:
        item: class, instance, module, or function to examine.
        names: str name or iterable of str names to look for.
        raise_error: whether to raise an `AttributeError` if the check fails.
            If None, `miller.configuration.RAISE_ERRORS` is used.
        match_all: whether all `names` must be found (True) or any (False). If
            None, `miller.configuration.MATCH_ALL` is used.

    Returns:
        Whether all (or any) of `names` are annotated in `item`.

    """
    return base.has_names(
        item, names, base.membership(_annotations(item)), raise_error, match_all
    )
