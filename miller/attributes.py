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
    

"""
from __future__ import annotations
from collections.abc import Callable, MutableSequence
import dataclasses
import inspect
import types
from typing import Any, Optional, Type

import camina 

from . import base
from . import configuration
from . import result


def has_attributes(
    item: Any, 
    attributes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' exist in 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not an attribute of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if some 'attributes' are not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether all 'attributes' exist in 'item'.
    
    """
    return base.has_elements(
        checker = is_attribute,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        elements = attributes)
    
def has_fields(
    item: dataclasses.dataclass | Type[dataclasses.dataclass], 
    fields: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'attributes' are fields in dataclass 'item'.

    Args:
        item (dataclasses.dataclass | Type[dataclasses.dataclass]): dataclass or 
            dataclass instance to examine.
        fields (MutableSequence[str]): names of fields to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'fields' are not an attribute of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'fields' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
    
    Raises:
        AttributeError: if some 'fields' are not fields of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
        TypeError: if 'item' is not a dataclass.
        
    Returns:
        bool: whether all 'fields' are fields in dataclass 'item'.
    
    """
    if dataclasses.identity.is_dataclass(item):
        return base.has_elements(
            checker = is_field,
            raise_error = raise_error,
            match_all = match_all,
            item = item,
            elements = fields)
    else:
        raise TypeError('item must be a dataclass')
   
def has_methods(
    item: Any, 
    methods: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'item' has 'methods' which are methods.

    Args:
        item (Any): object to examine.
        methods (MutableSequence[str]): names of methods to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'methods' are not an attribute of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'methods' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
                        
    Returns:
        bool: whether all 'methods' exist in 'item' and are methods.
        
    """
    return base.has_elements(
        checker = is_method,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        elements = methods)
  
def has_properties(
    item: Any, 
    properties: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'item' has 'properties' which are properties.

    Args:
        item (Any): object to examine.
        properties (MutableSequence[str]): names of properties to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'methods' are not an attribute of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'methods' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
            
    Returns:
        bool: whether all 'properties' exist in 'item' and are properties.
        
    """
    return base.has_elements(
        checker = is_property,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        elements = properties)
        
def has_traits(
    item: Any,
    attributes: Optional[MutableSequence[str]] = None,
    methods: Optional[MutableSequence[str]] = None,
    properties: Optional[MutableSequence[str]] = None, 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns if 'item' has 'attributes', 'methods' and 'properties'.

    Args:
        item (Any): object to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        methods (MutableSequence[str]): name(s) of methods to check.       
        properties (MutableSequence[str]): names of properties to check.
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
    kwargs = dict(raise_error = raise_error, match_all = match_all)
    return (
        has_attributes(item, attributes = attributes, **kwargs)
        and has_methods(item, methods = methods, **kwargs)
        and has_properties(item, properties = properties, **kwargs))
     
def is_attribute(
    item: dataclasses.dataclass | Type[dataclasses.dataclass],
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is an attribute of 'item'.

    Args:
        item (object | Type[Any]): class or instance of which 'attribute' is an
            attribute.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is an attribute.
        
    """
    return base.is_kind(
        checker = isinstance,
        raise_error = raise_error,
        item = item,
        kind = attribute)

def is_field(
    item: object | Type[Any],
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a field of 'item'.

    Args:
        item (dataclasses.dataclass | Type[dataclasses.dataclass]): dataclass or 
            dataclass instance to examine.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not a field of 'item' (True) or to simply return False in such 
            situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not a field of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is a field of 'item'.
        
    """
    return base.is_kind(
        checker = dataclasses.fields,
        raise_error = raise_error,
        item = getattr(item, attribute))
        
def is_method(
    item: object | Type[Any],
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a class attribute of 'item'.

    Args:
        item (object | Type[Any]): class or instance of which 'attribute' is an
            attribute.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is a class attribute of 'item'.
        
    """
    return base.is_kind(
        checker = inspect.ismethod,
        raise_error = raise_error,
        item = getattr(item, attribute))    
  
def is_property(
    item: object | Type[Any],
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a property of 'item'.

    Args:
        item (object | Type[Any]): class or instance of which 'attribute' is an
            attribute.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is a property of 'item'.
        
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

def is_variable(
    item: object | Type[Any],
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a data attribute of 'item'.

    Args:
        item (object | Type[Any]): class or instance of which 'attribute' is an
            attribute.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is a data attribute.
        
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

def is_class_attribute(
    item: object | Type[Any],
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a class attribute of 'item'.

    Args:
        item (object | Type[Any]): class or instance of which 'attribute' is an
            attribute.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is a class attribute.
        
    """
    if raise_error is None:
        raise_error = configuration.RAISE_ERRORS    
    item = item if inspect.isclass(item) else item.__class__
    if not hasattr(item, attribute) and raise_error:
        raise AttributeError(f'{attribute} is not an attribute of {item}')
    else:
        return hasattr(item, attribute)
    
def is_class_method(
    item: object | Type[Any],
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a class method of 'item'.

    The code used in this function is adapted from:
    https://stackoverflow.com/questions/19227724/check-if-a-function-uses-classmethod
    
    Args:
        attribute (str): name of method to examine.
        item (object | Type[Any]): class or instance of which 'attribute' is a
            method.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' is
            not a method of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not an method of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is a class method.
        
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
       
def is_class_variable(
    item: object | Type[Any],
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is a class attribute of 'item'.

    Args:
        item (object | Type[Any]): class or instance of which 'attribute' is an
            attribute.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is a class attribute.
        
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

def is_instance_attribute(
    item: object,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is an attribute of 'item'.

    Args:
        item (object): instance of which 'attribute' is an attribute.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is an attribute.
        
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
        item (object): instance of which 'attribute' is an attribute.
        attribute (str): name of method to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' is
            not a method of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not an method of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is an instance method.
        
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
  
def is_instance_variable(
    item: object,
    attribute: str, 
    raise_error: Optional[bool] = None) -> bool:
    """Returns if 'attribute' is an instance attribute of 'item'.

    Args:
        item (object): instance of which 'attribute' is an attribute.
        attribute (str): name of attribute to examine.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
    
    Raises:
        AttributeError: if 'attribute' is not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                  
    Returns:
        bool: whether 'attribute' is an instance attribute.
        
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
 
def list_annotations(
    item: object | types.ModuleType, 
    include_private: bool = False) -> list[Any]:
    """Returns list of type annotations.
    
    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[Any]: list of annotations of 'item'.
            
    """
    return list(map_annotations(
        item = item, 
        include_private = include_private).values())
   
def map_annotations(
    item: object | types.ModuleType, 
    include_private: bool = False) -> dict[str, Any]:
    """Returns dict of attributes of 'item' with type annotations.
    
    This function follows the best practices suggested for compatibility with
    Python 3.9 and before (without relying on the newer functionality of 3.10):
    https://docs.python.org/3/howto/annotations.html
    
    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        dict[str, Any]: dict of attributes in 'item' (keys are attribute names 
            and values are type annotations) that are type annotated.
            
    """
    if isinstance(item, type):
        annotations = item.__dict__.get('__annotations__', None)
    else:
        annotations = getattr(item, '__annotations__', None)
    if include_private:
        return annotations
    else:
        return camina.drop_privates_dict(annotations)
   
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
    item: dataclasses.dataclass | Type[dataclasses.dataclass], 
    include_private: bool = False) -> dict[str, dataclasses.Field]:
    """Returns whether 'attributes' exist in dataclass 'item'.

    Args:
        item (dataclasses.dataclass | Type[dataclasses.dataclass]): dataclass or 
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

def map_variables(
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
    variables = [
        a for a in attributes if a not in methods and a not in properties]
    values = [getattr(item, m) for m in variables]
    return dict(zip(variables, values))

def name_attributes(
    item: Any, 
    include_private: bool = False) -> list[str]:
    """Returns attribute names of 'item'.
    
    Args:
        item (object | Type[Any]): item to examine.
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
    item: dataclasses.dataclass | Type[dataclasses.dataclass], 
    include_private: bool = False) -> list[str]:
    """Returns whether 'attributes' exist in dataclass 'item'.

    Args:
        item (dataclasses.dataclass | Type[dataclasses.dataclass]): dataclass or 
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
        item (object | Type[Any]): item to examine.
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
  
def name_parameters(item: Type[Any]) -> list[str]:
    """Returns list of parameters based on annotations of 'item'.

    Args:
        item (Type[Any]): class to get parameters to.

    Returns:
        list[str]: names of parameters in 'item'.
        
    """          
    return list(item.__annotations__.keys())

def name_properties(
    item: Any, 
    include_private: bool = False) -> list[str]:
    """Returns method names of 'item'.
    
    Args:
        item (object | Type[Any]): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[str]: names of properties in 'item'.
            
    """
    if not inspect.isclass(item):
        item.__class__
    properties = [
        a for a in dir(item)
        if identify.identity.is_property(item, attribute = a)]
    if not include_private:
        properties = camina.drop_privates(properties)
    return properties

""" Private Functions """

def _check_trait(
    item: Any,
    attributes: MutableSequence[Any],
    raise_error: bool,
    match_all: bool,
    checker: Callable) -> bool:
    """Returns whether 'attributes' exist in 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not an attribute of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
        checker (Callable): function to call to determine if an attribute in
            'attributes' qualifies as the desired type.
            
    Raises:
        AttributeError: if some 'attributes' are not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether all 'attributes' exist in 'item'.
    
    """
    match_all = configuration.MATCH_ALL if None else match_all 
    scope = all if match_all else any
    kwargs = dict(raise_error = False)
    check = scope(checker(item, a, **kwargs) for a in attributes)  
    if not check and raise_error:
        raise AttributeError(
            f'Some of {attributes} are not attributes of {item}')
    elif not check:
        return False
    else:
        return True
