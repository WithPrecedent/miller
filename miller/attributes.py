"""
attributes: inspects attributes of classes, instances, or modules
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2020-2022, Corey Rayburn Yung
License: Apache-2.0

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Contents:
    Simple Type Checkers:
        is_container: returns if an item is a container but not a str.
        is_function: returns if an item is a function type.
        is_iterable: returns if an item is iterable but not a str.
        is_nested: dispatcher which returns if an item is a nested container.
        is_nested_dict: returns if an item is a nested dict.
        is_nested_sequence: returns if an item is a nested sequence.
        is_nested_set: returns if an item is a nested set.
        is_sequence: returns if an item is a sequence but not a str.
    Attribute Checkers:
        has_attributes
        has_methods
        has_properties
        has_signatures
        has_traits
        is_class_attribute: returns whether an attribute is a class 
            attribute.
        is_method: returns whether an attribute of a class is a method. 
        is_property 
        is_variable: returns whether an attribute of a class is an
            ordinary data variable. 
    File and Folder Checkers:
        is_file
        is_folder
        is_module
        is_path   
    
To Do:
    Adding parsing functionality to commented signature functions to find
        equivalence when one signature has subtypes of the other signature
        (e.g., one type annotation is 'dict' and the other is 'MutableMapping').
        It might be necessary to create a separate Signature-like class to 
        implement this functionality. This includes fixing or abandoning 
        'has_annotations' due to issues matching type annotations.
    Add support for Kinds once that system is complete.
    Add support for types (using type annotations) in the 'contains' function so
        that 'contains' can be applied to classes and not just instances.
    Add 'dispatcher' framework to 'contains' once the dispatcher framework is
        completed in the 'bobbie' package and the Kind system is completed in
        the nagata package. This should replace existing usages of python's
        singledispatch, which doesn't propertly deal with subtypes.
    
"""
from __future__ import annotations
from collections.abc import (
    Collection, Container, Hashable, Iterable, Mapping, MutableMapping, 
    MutableSequence, Sequence, Set)
import dataclasses
import functools
import inspect
import pathlib
import types
from typing import Any, Optional, Type, Union

import camina

from . import defaults
from . import objects


def has_attributes(
    item: Union[object, Type[Any]], 
    attributes: MutableSequence[str]) -> bool:
    """Returns whether 'attributes' exist in 'item'.

    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check to see
            if they exist in 'item'.
            
    Returns:
        bool: whether all 'attributes' exist in 'items'.
    
    """
    return all(hasattr(item, a) for a in attributes)

def has_fields(
    item: Union[dataclasses.dataclass, Type[dataclasses.dataclass]], 
    fields: MutableSequence[str]) -> bool:
    """Returns whether 'attributes' exist in dataclass 'item'.

    Args:
        item (Union[dataclasses.dataclass, Type[dataclasses.dataclass]]): 
            dataclass or dataclass instance to examine.
        fields (MutableSequence[str]): names of attributes to check to see
            if they exist in 'item'.
    
    Raises:
        TypeError: if 'item' is not a dataclass.
        
    Returns:
        bool: whether all 'attributes' exist in 'items'.
    
    """
    if dataclasses.is_dataclass(item):
        all_fields = [f.name for f in dataclasses.fields(item)]
        return all(a in all_fields for a in fields)
    else:
        raise TypeError('item must be a dataclass')

def has_methods(
    item: Union[object, Type[Any]], 
    methods: Union[str, MutableSequence[str]]) -> bool:
    """Returns whether 'item' has 'methods' which are methods.

    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        methods (Union[str, MutableSequence[str]]): name(s) of methods to check 
            to see if they exist in 'item' and are types.MethodType.
            
    Returns:
        bool: whether all 'methods' exist in 'items' and are types.MethodType.
        
    """
    methods = list(camina.iterify(methods))
    return all(is_method(item = item, attribute = m) for m in methods)

def has_properties(
    item: Union[object, Type[Any]], 
    properties: Union[str, MutableSequence[str]]) -> bool:
    """Returns whether 'item' has 'properties' which are properties.

    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        properties (MutableSequence[str]): names of properties to check to see 
            if they exist in 'item' and are property type.
            
    Returns:
        bool: whether all 'properties' exist in 'items'.
        
    """
    properties = list(camina.iterify(properties))
    return all(is_property(item = item, attribute = p) for p in properties)
    
def has_signatures(
    item: Union[object, Type[Any]], 
    signatures: Mapping[str, inspect.Signature]) -> bool:
    """Returns whether 'item' has 'signatures' of its methods.

    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        signatures (Mapping[str, inspect.Signature]): keys are the names of 
            methods and values are the corresponding method signatures.
            
    Returns:
        bool: whether all 'signatures' exist in 'items'.
        
    """
    keys = [a for a in dir(item) if is_method(item = item, attribute = a)]
    values = [inspect.signature(getattr(item, m)) for m in keys]
    item_signatures = dict(zip(keys, values))
    pass_test = True
    for name, parameters in signatures.items():
        if (name not in item_signatures or item_signatures[name] != parameters):
            pass_test = False
    return pass_test
   
def has_traits(
    item: Union[object, Type[Any]],
    attributes: Optional[MutableSequence[str]] = None,
    methods: Optional[MutableSequence[str]] = None,
    properties: Optional[MutableSequence[str]] = None) -> bool:
    """Returns if 'item' has 'attributes', 'methods' and 'properties'.

    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check to see
            if they exist in 'item'.
        methods (MutableSequence[str]): name(s) of methods to check to see if 
            they exist in 'item' and are types.MethodType.          
        properties (MutableSequence[str]): names of properties to check to see 
            if they exist in 'item' and are property type.
                          
    Returns:
        bool: whether all passed arguments exist in 'items'.    
    
    """
    if not inspect.isclass(item):
        item = item.__class__ 
    attributes = attributes or []
    methods = methods or []
    properties = properties or []
    signatures = signatures or {}
    return (
        has_attributes(item = item, attributes = attributes)
        and has_methods(item = item, methods = methods)
        and has_properties(item = item, properties = properties)
        and has_signatures(item = item, signatures = signatures))
 
def is_class_attribute(item: Union[object, Type[Any]], attribute: str) -> bool:
    """Returns if 'attribute' is a class attribute of 'item'."""
    if not inspect.isclass(item):
        item = item.__class__
    return (
        hasattr(item, attribute)
        and not is_method(item = item, attribute = attribute)
        and not is_property(item = item, attribute = attribute))
        
def is_method(item: Union[object, Type[Any]], attribute: Any) -> bool:
    """Returns if 'attribute' is a method of 'item'."""
    if isinstance(attribute, str):
        try:
            attribute = getattr(item, attribute)
        except AttributeError:
            return False
    return inspect.ismethod(attribute)
 
def is_property(item: Union[object, Type[Any]], attribute: Any) -> bool:
    """Returns if 'attribute' is a property of 'item'."""
    if not inspect.isclass(item):
        item = item.__class__
    if isinstance(attribute, str):
        try:
            attribute = getattr(item, attribute)
        except AttributeError:
            return False
    return isinstance(attribute, property)

def is_variable(item: Union[object, Type[Any]], attribute: str) -> bool:
    """Returns if 'attribute' is a simple data attribute of 'item'.

    Args:
        item (Union[object, Type[Any]]): [description]
        attribute (str): [description]

    Returns:
        bool: [description]
        
    """
    return (
        hasattr(item, attribute)
        and not objects.is_function(item = item)
        and not is_property(item = item, attribute = attribute))

# def has_annotations(
#     item: Union[object, Type[Any]], 
#     attributes: Mapping[str, Type[Any]]) -> bool:
#     """Returns whether 'attributes' exist in 'item' and are the right type.
    
#     Args:
#         item (Union[object, Type[Any]]): class or instance to examine.
#         attributes (dict[str, Type[Any]]): dict where keys are the attribute 
#             names and values are the expected types of whose named attributes.
            
#     Returns
#         bool: whether all of the 'attributes' exist in 'item' and are of the
#             proper type.
            
#     """
#     matched = True
#     if inspect.isclass(item):
#         for attribute, value in attributes.items():
#             if value is not None:
#                 try:
#                     testing = getattr(item, attribute)
#                     testing = item.__annotations__[testing]
#                 except AttributeError:
#                     return False
#                 try:
#                     if not issubclass(testing, value):
#                         return False
#                 except TypeError:
#                     pass
#     else:
#         for attribute, value in attributes.items():
#             if value is not None:
#                 try:
#                     testing = getattr(item, attribute)
#                 except AttributeError:
#                     return False
#                 try:
#                     if not isinstance(testing, value):
#                         return False
#                 except TypeError:
#                     pass
#     return matched  
  