"""
attributes: introspection tools for class and instance attributes
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
    This module contains the following types of inspectors:
        has
        is
        list
        map
        name
    Those relate to the following attributes of classes and instances:
        attributes
        fields
        methods
        properties
        traits
   
ToDo:
    Add functions for annotation instrospection.

"""
from __future__ import annotations
from collections.abc import MutableSequence
import dataclasses
import inspect
import types
from typing import Any, Optional

import camina 

from . import base
from . import configuration


def has_attributes(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item'.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item'.
    
    """
    return base.has_elements(
        item = item,
        attributes = attributes,
        checker = is_attribute,
        raise_error = raise_error,
        match_all = match_all)

def has_class_attributes(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item' as class attributes.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
    
    """
    return base.has_elements(
        item = item,
        attributes = attributes,
        checker = is_class_attribute,
        raise_error = raise_error,
        match_all = match_all)

def has_class_methods(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item' as class methods.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
    
    """
    return base.has_elements(
        item = item,
        attributes = attributes,
        checker = is_class_method,
        raise_error = raise_error,
        match_all = match_all)

def has_class_objects(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item' as class objects.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
    
    """
    return base.has_elements(
        item = item,
        attributes = attributes,
        checker = is_class_object,
        raise_error = raise_error,
        match_all = match_all)
               
def has_fields(
    item: dataclasses.dataclass | type[dataclasses.dataclass], 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' are fields in dataclass 'item'.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
        TypeError: if 'item' is not a dataclass.
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
    
    """
    if dataclasses.identity.is_dataclass(item):
        return base.has_elements(
            item = item,
            attributes = attributes,
            checker = is_field,
            raise_error = raise_error,
            match_all = match_all)
    else:
        raise TypeError('item must be a dataclass')

def has_instance_attributes(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item' as instance attributes.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
    
    """
    return base.has_elements(
        item = item,
        attributes = attributes,
        checker = is_instance_attribute,
        raise_error = raise_error,
        match_all = match_all)

def has_instance_methods(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item' as instance methods.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
    
    """
    return base.has_elements(
        item = item,
        attributes = attributes,
        checker = is_instance_method,
        raise_error = raise_error,
        match_all = match_all)

def has_instance_objects(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item' as instance objects.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
    
    """
    return base.has_elements(
        item = item,
        attributes = attributes,
        checker = is_instance_object,
        raise_error = raise_error,
        match_all = match_all)
        
def has_methods(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item' as methods.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
        
    """
    return base.has_elements(
        item = item,
        attributes = attributes,
        checker = is_method,
        raise_error = raise_error,
        match_all = match_all)
  
def has_properties(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item' as properties.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
        
    """
    return base.has_elements(
        item = item,
        attributes = attributes,
        checker = is_property,
        raise_error = raise_error,
        match_all = match_all)
        
def has_traits(
    item: Any,
    attributes: Optional[MutableSequence[str]] = None,
    methods: Optional[MutableSequence[str]] = None,
    properties: Optional[MutableSequence[str]] = None, 
    objects: Optional[MutableSequence[str]] = None,
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns if 'item' has all or some of the passed traits.

    Args:
        item (Any): object to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        methods (MutableSequence[str]): name(s) of methods to check.       
        properties (MutableSequence[str]): names of properties to check.
        objects (MutableSequence[str]): names of objects to check.
        raise_error (Optional[bool]): whether to raise an error if any of the 
            traits are not an attribute of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in the traits must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
                          
    Returns:
        bool: whether all passed arguments exist in 'item'.    
    
    """
    attributes = attributes or []
    methods = methods or []
    properties = properties or []
    objects = objects or []
    kwargs = dict(raise_error = raise_error, match_all = match_all)
    return (
        has_attributes(item, attributes = attributes, **kwargs)
        and has_methods(item, attributes = methods, **kwargs)
        and has_properties(item, attributes = properties, **kwargs)
        and has_objects(item, attributes = objects, **kwargs))
  
def has_objects(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item' as simple data objects.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
        
    """
    return base.has_elements(
        item = item,
        attributes = attributes,
        checker = is_object,
        raise_error = raise_error,
        match_all = match_all)
             
def is_attribute(
    item: Any,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is an attribute of 'item'.

    Args:
        item (Any): class or instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                  
    Returns:
        bool: whether 'attribute' is an attribute.
        
    """
    return base.is_kind_class(
        item = item,
        kind = attribute,
        checker = hasattr,
        raise_error = raise_error)

def is_class_attribute(
    item: Any,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a class attribute of 'item'.

    Args:
        item (Any): class or instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                  
    Returns:
        bool: whether 'attribute' is an attribute and the appropriate type.
        
    """ 
    item = item if inspect.isclass(item) else item.__class__
    return base.is_kind_class(
        item = item,
        kind = attribute,
        checker = hasattr,
        raise_error = raise_error)

def is_class_method(
    item: Any,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a class method of 'item'.

    The code used in this function is adapted from:
    https://stackoverflow.com/questions/19227724/check-if-a-function-uses-classmethod
    
    Args:
        item (Any): class or instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                  
    Returns:
        bool: whether 'attribute' is an attribute and the appropriate type.
        
    """
    if raise_error is None:
        raise_error = configuration.RAISE_ERRORS    
    item = item if inspect.isclass(item) else item.__class__
    if not hasattr(item, attribute) and raise_error:
        raise AttributeError(f'{attribute} is not an method of {item}')
    elif is_method(item, attribute):
        method = getattr(item, attribute)
        bound_to = getattr(method, '__self__', None)
        if not isinstance(bound_to, type):
            return False
        name = method.__name__
        for cls in bound_to.__mro__:
            descriptor = vars(cls).get(name)
            if descriptor is not None:
                return isinstance(descriptor, classmethod)
    return False    
       
def is_class_object(
    item: Any,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a class object of 'item'.

    Args:
        item (Any): class or instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                  
    Returns:
        bool: whether 'attribute' is an attribute and the appropriate type.
        
    """
    if raise_error is None:
        raise_error = configuration.RAISE_ERRORS    
    owner = item if inspect.isclass(item) else item.__class__
    if not hasattr(item, attribute) and raise_error:
        raise AttributeError(f'{attribute} is not an attribute of {item}')
    else:
        return (
            hasattr(owner, attribute)
            and not is_method(item, attribute, raise_error = False)
            and not is_property(owner, attribute, raise_error = False))
    
def is_field(
    item: Any,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a field of 'item'.

    Args:
        item (dataclasses.dataclass | type[dataclasses.dataclass]): dataclass or 
            dataclass instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
        TypeError: if 'item' is not a dataclass.
                  
    Returns:
        bool: whether 'attribute' is an attribute and the appropriate type.
        
    """
    if dataclasses.identity.is_dataclass(item):
        return base.is_kind_class(
            checker = dataclasses.fields,
            raise_error = raise_error,
            item = getattr(item, attribute))
    else:
        raise TypeError('item must be a dataclass')

def is_instance_attribute(
    item: object,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is an instance attribute of 'item'.

    Args:
        item (Any): class or instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                  
    Returns:
        bool: whether 'attribute' is an attribute and the appropriate type.
        
    """
    if raise_error is None:
        raise_error = configuration.RAISE_ERRORS
    owner = item if inspect.isclass(item) else item.__class__
    if not hasattr(item, attribute) and raise_error:
        raise AttributeError(f'{attribute} is not an attribute of {item}')
    else:
        return (
            hasattr(item, attribute) 
            and not is_class_attribute(owner, attribute, raise_error = False))
 
def is_instance_method(
    item: object,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is an instance method of 'item'.

    Args:
        item (Any): class or instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                  
    Returns:
        bool: whether 'attribute' is an attribute and the appropriate type.
        
    """
    if raise_error is None:
        raise_error = configuration.RAISE_ERRORS    
    if not hasattr(item, attribute) and raise_error:
        raise AttributeError(f'{attribute} is not an method of {item}')
    else:
        return (
            hasattr(item, attribute) 
            and is_method(item, attribute, raise_error = False)
            and not is_class_method(item, attribute, raise_error = False))
  
def is_instance_object(
    item: object,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is an instance object of 'item'.

    Args:
        item (Any): class or instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                  
    Returns:
        bool: whether 'attribute' is an attribute and the appropriate type.
        
    """
    if raise_error is None:
        raise_error = configuration.RAISE_ERRORS    
    owner = item if inspect.isclass(item) else item.__class__
    if not hasattr(item, attribute) and raise_error:
        raise AttributeError(f'{attribute} is not an attribute of {item}')
    else:
        return (
            hasattr(item, attribute)
            and not is_class_attribute(owner, attribute, raise_error = False)
            and not is_method(item, attribute, raise_error = False)
            and not is_property(item, attribute, raise_error = False))
         
def is_method(
    item: Any,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a method of 'item'.

    Args:
        item (Any): class or instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                  
    Returns:
        bool: whether 'attribute' is an attribute and the appropriate type.
        
    """
    return base.is_kind_class(
        checker = inspect.ismethod,
        raise_error = raise_error,
        item = getattr(item, attribute))    
  
def is_property(
    item: Any,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a property of 'item'.

    Args:
        item (Any): class or instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                  
    Returns:
        bool: whether 'attribute' is an attribute and the appropriate type.
        
    """
    if raise_error is None:
        raise_error = configuration.RAISE_ERRORS    
    item = item if inspect.isclass(item) else item.__class__
    if not hasattr(item, attribute) and raise_error:
        raise AttributeError(f'{attribute} is not an attribute of {item}')
    else:
        return (
            hasattr(item, attribute) 
            and isinstance(getattr(item, attribute), property))

def is_object(
    item: Any,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a data object of 'item'.

    Args:
        item (Any): class or instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                  
    Returns:
        bool: whether 'attribute' is an attribute and the appropriate type.
        
    """
    if raise_error is None:
        raise_error = configuration.RAISE_ERRORS    
    if not hasattr(item, attribute) and raise_error:
        raise AttributeError(f'{attribute} is not an attribute of {item}')
    else:
        return(
            hasattr(item, attribute)
            and not is_method(item, attribute, raise_error = False)
            and not is_property(item, attribute, raise_error = False))

def map_attributes(
    item: object, 
    include_private: bool = False) -> dict[str, Any]:
    """Returns dict of attributes of 'item'.
    
    Args:
        item (Any): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        dict[str, Any]: dict of attributes in 'item' (keys are attribute names 
            and values are attribute values).
            
    """
    attributes = name_attributes(item, include_private = include_private)
    values = [getattr(item, m) for m in attributes]
    return dict(zip(attributes, values))

def map_fields(
    item: dataclasses.dataclass | type[dataclasses.dataclass], 
    include_private: bool = False) -> dict[str, dataclasses.Field]:
    """Returns whether 'attributes' exist in dataclass 'item'.

    Args:
        item (dataclasses.dataclass | type[dataclasses.dataclass]): dataclass or 
            dataclass instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.    
    Raises:
        TypeError: if 'item' is not a dataclass.
        
    Returns:
        dict[str, dataclasses.Field]: dict of fields in 'item' (keys are 
            attribute names and values are dataclass fields).
    
    """
    if dataclasses.identify.identity.is_dataclass(item):
        attributes = {f.name: f for f in dataclasses.fields(item)}
        if not include_private:
            attributes = camina.drop_privates(attributes)
        return attributes
    else:
        raise TypeError('item must be a dataclass')
  
def map_methods(
    item: Any, 
    include_private: bool = False) -> dict[str, types.MethodType]:
    """Returns dict of methods of 'item'.
    
    Args:
        item (Any): object to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.

    Returns:
        dict[str, types.MethodType]: dict of methods in 'item' (keys are method 
            names and values are methods).
        
    """ 
    methods = name_methods(item, include_private = include_private)
    return [getattr(item, m) for m in methods]

def map_properties(
    item: object, 
    include_private: bool = False) -> dict[str, Any]:
    """Returns properties of 'item'.

    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.

    Returns:
        dict[str, Any]: dict of properties in 'item' (keys are property names 
            and values are property values).
        
    """    
    properties = name_properties(item, include_private = include_private)
    values = [getattr(item, p) for p in properties]
    return dict(zip(properties, values))

def map_signatures(
    item: Any, 
    include_private: bool = False) -> dict[str, inspect.Signature]:
    """Returns dict of method signatures of 'item'.

    Args:
        item (Any): object to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.

    Returns:
        dict[str, inspect.Signature]: dict of method signatures in 'item' (keys 
            are method names and values are method signatures).
                   
    """ 
    methods = name_methods(item, include_private = include_private)
    signatures = [inspect.signature(getattr(item, m)) for m in methods]
    return dict(zip(methods, signatures))

def map_objects(
    item: object, 
    include_private: bool = False) -> dict[str, Any]:
    """Returns dict of attributes of 'item' that are not methods or properties.
    
    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        dict[str, Any]: dict of attributes in 'item' (keys are attribute names 
            and values are attribute values) that are not methods or properties.
            
    """
    attributes = name_attributes(item, include_private = include_private)
    methods = name_methods(item, include_private = include_private)
    properties = name_properties(item, include_private = include_private)
    objects = [
        a for a in attributes if a not in methods and a not in properties]
    values = [getattr(item, m) for m in objects]
    return dict(zip(objects, values))

def name_attributes(
    item: Any, 
    include_private: bool = False) -> list[str]:
    """Returns attribute names of 'item'.
    
    Args:
        item (Any): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[str]: names of attributes in 'item'.
            
    """
    names = dir(item)
    if not include_private:
        names = camina.drop_privates(names)
    return names
      
def name_fields(
    item: dataclasses.dataclass | type[dataclasses.dataclass], 
    include_private: bool = False) -> list[str]:
    """Returns whether 'attributes' exist in dataclass 'item'.

    Args:
        item (dataclasses.dataclass | type[dataclasses.dataclass]): dataclass or 
            dataclass instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.    
    Raises:
        TypeError: if 'item' is not a dataclass.
        
    Returns:
        list[str]: names of fields in 'item'.
    
    """
    if dataclasses.identity.is_dataclass(item):
        attributes = [f.name for f in dataclasses.fields(item)]
        if not include_private:
            attributes = camina.drop_privates(attributes)
        return attributes
    else:
        raise TypeError('item must be a dataclass')
     
def name_methods(
    item: Any, 
    include_private: bool = False) -> list[str]:
    """Returns method names of 'item'.
    
    Args:
        item (Any): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[str]: names of methods in 'item'.
            
    """
    methods = [
        a for a in dir(item)
        if is_method(item, attribute = a)]
    if not include_private:
        methods = camina.drop_privates(methods)
    return methods
  
def name_parameters(item: type[Any]) -> list[str]:
    """Returns list of parameters based on annotations of 'item'.

    Args:
        item (type[Any]): class to get parameters to.

    Returns:
        list[str]: names of parameters in 'item'.
        
    """          
    return list(item.__annotations__.keys())

def name_properties(
    item: Any, 
    include_private: bool = False) -> list[str]:
    """Returns method names of 'item'.
    
    Args:
        item (Any): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[str]: names of properties in 'item'.
            
    """
    if not inspect.isclass(item):
        item.__class__
    properties = [
        a for a in dir(item)
        if is_property(item, attribute = a)]
    if not include_private:
        properties = camina.drop_privates(properties)
    return properties


# def list_annotations(
#     item: Any, 
#     include_private: bool = False, 
#     raise_error: Optional[bool] = None) -> list[Any]:
#     """Returns list of type annotations in 'item'.
    
#     Args:
#         item (Any): class or instance to examine.
#         include_private (bool): whether to include items that begin with '_'
#             (True) or to exclude them (False). Defauls to False.
#         raise_error (Optional[bool]): whether to raise an error if no matches
#             are found in 'item' or to simply return False in such situations. 
#             Defaults to None, which means the global 'miller.RAISE_ERRORS' 
#             setting will be used.

#     Raises:
#         AttributeError: if there are no matches in 'item' and 'raise_error' is 
#             True (or if it is None and the global setting is True).    
                                            
#     Returns:
#         list[Any]: list of the appropriate types in 'item'.
            
#     """
#     return list(map_annotations(
#         item = item, 
#         include_private = include_private).values())
   
# def map_annotations(
#     item: object | types.ModuleType, 
#     include_private: bool = False) -> dict[str, Any]:
#     """Returns dict of attributes of 'item' with type annotations.
    
#     This function follows the best practices suggested for compatibility with
#     Python 3.9 and before (without relying on the newer functionality of 3.10):
#     https://docs.python.org/3/howto/annotations.html
    
#     Args:
#         item (object): instance to examine.
#         include_private (bool): whether to include items that begin with '_'
#             (True) or to exclude them (False). Defauls to False.
                        
#     Returns:
#         dict[str, Any]: dict of attributes in 'item' (keys are attribute names 
#             and values are type annotations) that are type annotated.
            
#     """
#     if isinstance(item, type):
#         annotations = item.__dict__.get('__annotations__', None)
#     else:
#         annotations = getattr(item, '__annotations__', None)
#     if include_private:
#         return annotations
#     else:
#         return camina.drop_privates_dict(annotations)
   