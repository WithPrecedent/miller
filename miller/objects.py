"""
objects: inspects objects and types
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


def is_container(item: Union[object, Type[Any]]) -> bool:
    """Returns if 'item' is a container and not a str.
    
    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a container but not a str.
        
    """  
    if not inspect.isclass(item):
        item = item.__class__ 
    return issubclass(item, Container) and not issubclass(item, str)

def is_dict(item: Union[object, Type[Any]]) -> bool:
    """Returns if 'item' is a mutable mapping (generic dict type).
    
    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a mutable mapping type.
        
    """  
    if not inspect.isclass(item):
        item = item.__class__ 
    return isinstance(item, MutableMapping) 

def is_function(item: Union[object, Type[Any]]) -> bool:
    """Returns if 'item' is a function type.
    
    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a function type.
        
    """  
    return isinstance(item, types.FunctionType)
   
def is_iterable(item: Union[object, Type[Any]]) -> bool:
    """Returns if 'item' is iterable and is NOT a str type.
    
    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        
    Returns:
        bool: if 'item' is iterable but not a str.
        
    """ 
    if not inspect.isclass(item):
        item = item.__class__ 
    return issubclass(item, Iterable) and not issubclass(item, str)

def is_list(item: Union[object, Type[Any]]) -> bool:
    """Returns if 'item' is a mutable sequence (generic list type).
    
    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a mutable list type.
        
    """
    if not inspect.isclass(item):
        item = item.__class__ 
    return isinstance(item, MutableSequence)

def is_sequence(item: Union[object, Type[Any]]) -> bool:
    """Returns if 'item' is a sequence and is NOT a str type.
    
    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a sequence but not a str.
        
    """ 
    if not inspect.isclass(item):
        item = item.__class__ 
    return issubclass(item, Sequence) and not issubclass(item, str) 
        
def is_set(item: Union[object, Type[Any]]) -> bool:
    """Returns if 'item' is a Set (including generic type sets).
    
    Args:
        item (Union[object, Type[Any]]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a set.
        
    """ 
    if not inspect.isclass(item):
        item = item.__class__ 
    return issubclass(item, Set)
