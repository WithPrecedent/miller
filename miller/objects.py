"""
objects: introspection tools for objects and classes
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

        
ToDo:


"""
from __future__ import annotations
from collections.abc import (
    Container, Iterable, Mapping, MutableMapping, MutableSequence,  Set)
import dataclasses
import functools
import inspect
import pathlib
import sys
import types
from typing import Any, Optional, Type

import camina
import nagata


def has_attributes(
    item: object | Type[Any], 
    attributes: MutableSequence[str]) -> bool:
    """Returns whether 'attributes' exist in 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check to see
            if they exist in 'item'.
            
    Returns:
        bool: whether all 'attributes' exist in 'items'.
    
    """
    return all(hasattr(item, a) for a in attributes)

def has_fields(
    item: dataclasses.dataclass | Type[dataclasses.dataclass], 
    fields: MutableSequence[str]) -> bool:
    """Returns whether 'attributes' exist in dataclass 'item'.

    Args:
        item (dataclasses.dataclass | Type[dataclasses.dataclass]): 
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
    item: object | Type[Any], 
    methods: str | MutableSequence[str]) -> bool:
    """Returns whether 'item' has 'methods' which are methods.

    Args:
        item (object | Type[Any]): class or instance to examine.
        methods (str | MutableSequence[str]): name(s) of methods to check 
            to see if they exist in 'item' and are types.MethodType.
            
    Returns:
        bool: whether all 'methods' exist in 'items' and are types.MethodType.
        
    """
    methods = list(camina.iterify(methods))
    return all(identify.is_method(item, attribute = m) for m in methods)
  
def has_properties(
    item: object | Type[Any], 
    properties: str | MutableSequence[str]) -> bool:
    """Returns whether 'item' has 'properties' which are properties.

    Args:
        item (object | Type[Any]): class or instance to examine.
        properties (MutableSequence[str]): names of properties to check to see 
            if they exist in 'item' and are property type.
            
    Returns:
        bool: whether all 'properties' exist in 'items'.
        
    """
    properties = list(camina.iterify(properties))
    return all(identify.is_property(item, attribute = p) for p in properties)
    
def has_signatures(
    item: object | Type[Any], 
    signatures: Mapping[str, inspect.Signature]) -> bool:
    """Returns whether 'item' has 'signatures' of its methods.

    Args:
        item (object | Type[Any]): class or instance to examine.
        signatures (Mapping[str, inspect.Signature]): keys are the names of 
            methods and values are the corresponding method signatures.
            
    Returns:
        bool: whether all 'signatures' exist in 'items'.
        
    """
    keys = [a for a in dir(item) if identify.is_method(item, attribute = a)]
    values = [inspect.signature(getattr(item, m)) for m in keys]
    item_signatures = dict(zip(keys, values))
    pass_test = True
    for name, parameters in signatures.items():
        if (name not in item_signatures or item_signatures[name] != parameters):
            pass_test = False
    return pass_test
   
def has_traits(
    item: object | Type[Any],
    attributes: Optional[MutableSequence[str]] = None,
    methods: Optional[MutableSequence[str]] = None,
    properties: Optional[MutableSequence[str]] = None) -> bool:
    """Returns if 'item' has 'attributes', 'methods' and 'properties'.

    Args:
        item (object | Type[Any]): class or instance to examine.
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
        has_attributes(item, attributes = attributes)
        and has_methods(item, methods = methods)
        and has_properties(item, properties = properties)
        and has_signatures(item, signatures = signatures))
 
def is_class_attribute(item: object | Type[Any], /, attribute: str) -> bool:
    """Returns if 'attribute' is a class attribute of 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attribute (str): name of attribute to examine.

    Returns:
        bool: where 'attribute' is a class attribute.
        
    """    
    if not inspect.isclass(item):
        item.__class__
    return (
        hasattr(item, attribute)
        and not is_method(item, attribute = attribute)
        and not is_property(item, attribute = attribute))
      
def is_container(item: object | Type[Any]) -> bool:
    """Returns if 'item' is a container and not a str.
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a container but not a str.
        
    """  
    if not inspect.isclass(item):
        item = item.__class__
    return issubclass(item, Container) and not issubclass(item, str)

def is_dict(item: object | Type[Any]) -> bool:
    """Returns if 'item' is a mutable mapping (generic dict type).
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a mutable mapping type.
        
    """  
    if not inspect.isclass(item):
        item = item.__class__
    return isinstance(item, MutableMapping) 

def is_function(item: object | Type[Any]) -> bool:
    """Returns if 'item' is a function type.
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a function type.
        
    """  
    return isinstance(item, types.FunctionType)
   
def is_iterable(item: object | Type[Any]) -> bool:
    """Returns if 'item' is iterable and is NOT a str type.
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is iterable but not a str.
        
    """ 
    if not inspect.isclass(item):
        item = item.__class__
    return issubclass(item, Iterable) and not issubclass(item, str)

def is_list(item: object | Type[Any]) -> bool:
    """Returns if 'item' is a mutable sequence (generic list type).
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a mutable list type.
        
    """
    if not inspect.isclass(item):
        item = item.__class__
    return isinstance(item, MutableSequence)
  
def is_method(item: object | Type[Any], attribute: Any) -> bool:
    """Returns if 'attribute' is a method of 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attribute (str): name of attribute to examine.

    Returns:
        bool: where 'attribute' is a method of 'item'.
        
    """ 
    if isinstance(attribute, str):
        try:
            attribute = getattr(item, attribute)
        except AttributeError:
            return False
    return inspect.ismethod(attribute)

def is_property(item: object | Type[Any], attribute: Any) -> bool:
    """Returns if 'attribute' is a property of 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attribute (str): name of attribute to examine.

    Returns:
        bool: where 'attribute' is a property of 'item'.
        
    """ 
    if not inspect.isclass(item):
        item.__class__
    if isinstance(attribute, str):
        try:
            attribute = getattr(item, attribute)
        except AttributeError:
            return False
    return isinstance(attribute, property)
 
def is_variable(
    item: object | Type[Any] | types.ModuleType, 
    attribute: str) -> bool:
    """Returns if 'attribute' is a simple data attribute of 'item'.

    Args:
        item (object | Type[Any] | types.ModuleType): class or instance to 
            examine.
        attribute (str): name of attribute to examine.

    Returns:
        bool: where 'attribute' is a simple variable (and not a method or 
            property) or 'item'.
        
    """ 
    return (
        hasattr(item, attribute)
        and not is_function(item)
        and not is_property(item, attribute = attribute))

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
    if dataclasses.identify.is_dataclass(item):
        attributes = {f.name: f for f in dataclasses.fields(item)}
        if not include_private:
            attributes = camina.drop_privates(attributes)
        return attributes
    else:
        raise TypeError('item must be a dataclass')
  
def map_methods(
    item: object | Type[Any], 
    include_private: bool = False) -> dict[str, types.MethodType]:
    """Returns dict of methods of 'item'.
    
    Args:
        item (object | Type[Any]): class or instance to examine.
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
    item: object | Type[Any], 
    include_private: bool = False) -> dict[str, inspect.Signature]:
    """Returns dict of method signatures of 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
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
    item: object | Type[Any], 
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
    if dataclasses.is_dataclass(item):
        attributes = [f.name for f in dataclasses.fields(item)]
        if not include_private:
            attributes = camina.drop_privates(attributes)
        return attributes
    else:
        raise TypeError('item must be a dataclass')
     
def name_methods(
    item: object | Type[Any], 
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
        if identify.is_method(item, attribute = a)]
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
    item: object | Type[Any], 
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
        if identify.is_property(item, attribute = a)]
    if not include_private:
        properties = camina.drop_privates(properties)
    return properties
